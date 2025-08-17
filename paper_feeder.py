import os
import schedule
import time
# from fetch_pubmed_rss import fetch_pubmed_rss
# from fetch_arxiv_rss import fetch_arxiv_rss
from paper_reader_kernel import ask_deepseek
from datetime import datetime
from universal_rss_fetcher2 import UniversalRSSFetcher, fetch_rss_universal
from paper_reader_kernel import run_shell_command

"""Automated RSS feeder for arXiv and PubMed.

This script fetches the latest papers, stores the raw RSS content in Markdown/PDF,
and asks an LLM to create concise summaries.
"""

PROMPT_SUMMARY = 'For each article, keep the full title, write a 1-2 sentence summary focusing on objective, method, and key findings, and clearly indicate whether the study appears to be high-impact based on novelty or significance.'
ITERATION_NUM = 3

def job(summarize=True):

    timestamp = datetime.now().strftime('%Y%m%d_%H')
    feed_dir = f'./feed_folder/feeds_{timestamp}'
    os.makedirs(feed_dir, exist_ok=True)

    fetcher = UniversalRSSFetcher()
    ###############################################
    # First fetch all RSS feeds
    fetch_results = []

    # arxiv
    arxiv_categories = {
        'cs.AI': 'https://export.arxiv.org/rss/cs.AI',  # 人工智能
        'cs.LG': 'https://export.arxiv.org/rss/cs.LG',  # 机器学习
        # 'cs.CV': 'https://export.arxiv.org/rss/cs.CV',  # 计算机视觉
        # 'cs.CL': 'https://export.arxiv.org/rss/cs.CL',  # 计算语言学
        # 'cs.IR': 'https://export.arxiv.org/rss/cs.IR',  # 信息检索
        # 'stat.ML': 'https://export.arxiv.org/rss/stat.ML',  # 统计机器学习
        # 'q-bio.QM': 'https://export.arxiv.org/rss/q-bio.QM',  # 定量方法
        # 'physics.med-ph': 'https://export.arxiv.org/rss/physics.med-ph'  # 医学物理
    }
    for category, url in arxiv_categories.items():
        original_md = f"{feed_dir}/arxiv_org{category}_{timestamp}.md"
        original_pdf = f"{feed_dir}/arxiv_org{category}_{timestamp}.pdf"
        summary_md = f"{feed_dir}/arxiv_summary{category}_{timestamp}.md"
        summary_pdf = summary_md.replace('.md', '.pdf')

        print(f"\n正在抓取 arXiv {category} 类别...")
        result = fetcher.fetch_universal_rss(
            url,
            source_type="arxiv",
            md_file=original_md
        )
        print(f"arXiv {category} RSS抓取完成，共{len(result.split('['))-1}篇论文")
        fetch_results.append((result, original_md, original_pdf, summary_md, summary_pdf))

    ##############################################
    # First combine all markdown content into one file
    merged_md = f"{feed_dir}/arxiv_merged_{timestamp}.md"
    with open(merged_md, 'w', encoding='utf-8') as f:
        for result, _, _, _, _ in fetch_results:
            f.write(result + "\n\n")
    
    # Convert combined markdown to PDF
    merged_pdf = f"{feed_dir}/arxiv_merged_{timestamp}.pdf"
    run_shell_command("md2pdf", merged_md, merged_pdf)
    ##############################################
    
    #############################################
    # Then process all results with deepseek if summarize is enabled
    if summarize:
        for result, _, _, summary_md, summary_pdf in fetch_results:
            ask_deepseek(
                PROMPT_SUMMARY,
                result,
                summary_md,
                summary_pdf,
                iteration_num=ITERATION_NUM,
            )
    #############################################

job()
schedule.every().day.at("08:15").do(job)
schedule.every().day.at("20:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)