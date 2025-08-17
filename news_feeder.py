from universal_rss_fetcher2 import UniversalRSSFetcher
import datetime
from paper_reader_kernel import ask_deepseek
import time

ITERATION_NUM = 3
PROMPT_SUMMARY = """你是一个专业的文章摘要员，你的任务是根据文章的内容，生成一个摘要。"""

# Add timing measurement
start_time = time.time()

fetcher = UniversalRSSFetcher()
result = fetcher.fetch_universal_rss(
    "https://feedx.net/rss/bbc.xml",
    source_type="news",
    md_file=f"./tmp/news_bbc_{datetime.date.today().strftime('%Y%m%d')}.md"
)
summary_md = f"./tmp/news_bbc_{datetime.date.today().strftime('%Y%m%d')}_summary.md"
summary_pdf = f"./tmp/news_bbc_{datetime.date.today().strftime('%Y%m%d')}_summary.pdf"

ask_deepseek(
    PROMPT_SUMMARY,
    result,
    summary_md,
    summary_pdf,
    iteration_num=ITERATION_NUM,
    llm_model="deepseek-r1:latest", 
    llm_model_merge="deepseek-r1:70b"
)

end_time = time.time()
print(f"Total execution time: {end_time - start_time:.2f} seconds")
