from universal_rss_fetcher2 import UniversalRSSFetcher
import datetime
from paper_reader_kernel import ask_deepseek
import time
import schedule
from typing import Dict, List
import os

# Constants
ITERATION_NUM = 3
PROMPT_SUMMARY = """You are a professional financial news analyst and article summarizer. Please analyze and summarize the main content of the article, focusing on:
                    1. Market trends and changes in key economic indicators
                    2. Major corporate events and strategic adjustments
                    3. Potential market impacts of policy changes
                    4. Global economic situation analysis

                    Please output the summary in professional and concise language."""

# PROMPT_SUMMARY_CN = """你是一个专业的财经新闻分析师和文章摘要员。请分析并总结文章的主要内容，重点关注:
#                     1. 市场趋势和重要经济指标变化
#                     2. 公司重大事件和战略调整
#                     3. 政策变动对市场的潜在影响
#                     4. 全球经济形势分析

#                     请用专业且简洁的语言输出摘要。"""

# News source configuration
NEWS_SOURCES = {
    "bbc": "https://feedx.net/rss/bbc.xml",
    # "reuters_business": "https://feeds.reuters.com/reuters/businessNews",
    # "wsj": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "ft": "https://www.ft.com/rss/home",
    "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
    # Chinese media sources
    "xinhua": "http://www.xinhuanet.com/english/rss/chinarss.xml",
    "caixin": "http://english.caixin.com/rss/feed.xml",
    "scmp": "https://www.scmp.com/rss/91/feed",
    "china_daily": "http://www.chinadaily.com.cn/rss/china_rss.xml",
    "sina_finance": "https://feedx.net/rss/sinafinance.xml"
}
def process_news_source(source_name: str, url: str) -> Dict[str, str]:
    """Process a single news source and return file paths"""
    date_str = datetime.date.today().strftime('%Y%m%d')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H')
    feed_dir = f'./news_feeds/feeds_{timestamp}'

    # Create news_feeds directory if it doesn't exist
    os.makedirs(feed_dir, exist_ok=True)
    return {
        'raw_md': f"{feed_dir}/news_{source_name}_{date_str}.md",
        'summary_md': f"{feed_dir}/news_{source_name}_{date_str}_summary.md",
        'summary_pdf': f"{feed_dir}/news_{source_name}_{date_str}_summary.pdf"
    }

def job(summarize=True):
    start_time = time.time()
    fetcher = UniversalRSSFetcher()

    for source_name, url in NEWS_SOURCES.items():
        files = process_news_source(source_name, url)
        
        # Fetch and process news
        result = fetcher.fetch_universal_rss(
            url,
            source_type="news",
            md_file=files['raw_md']
        )

        # # Generate summary
        if summarize:
            ask_deepseek(
                PROMPT_SUMMARY,
                result,
                files['summary_md'],
                files['summary_pdf'],
                iteration_num=ITERATION_NUM,
                llm_model="deepseek-r1:latest",
                llm_model_merge="deepseek-r1:70b"
            )

    execution_time = time.time() - start_time
    print(f"News processing completed in {execution_time:.2f} seconds")

job()
schedule.every().day.at("03:00").do(job)
# schedule.every().day.at("20:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
