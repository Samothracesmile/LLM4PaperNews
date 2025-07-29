import os
from fetch_pubmed_rss import fetch_pubmed_rss
from paper_reader_kernel import ask_deepseek

from datetime import datetime
import schedule
import time

from fetch_arxiv_rss import fetch_arxiv_rss




def job():
    
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime('%Y%m%d_%H:%M')
    timestamp = datetime.now().strftime('%Y%m%d_%H')
    
    
    feed_dir = f'/ifs/loni/faculty/shi/spectrum/yxia/github_2025/LLM/LLM4PaperNews/feed_folder/feeds_{timestamp}'
    os.makedirs(feed_dir, exist_ok=True)
    
    ###############################################
    # arxiv
    categories = [
        ('cs.AI', 'ARTIFICIAL INTELLIGENCE', 1),
        ('cs.CL', 'COMPUTATION AND LANGUAGE', 2),
        ('cs.IR', 'INFORMATION RETRIEVAL', 3),
        ('cs.LG', 'COMPUTER SCIENCE - MACHINE LEARNING', 4),
        ('stat.ML', 'STATISTICS - MACHINE LEARNING', 5),
    ]


    for cat_code, cat_name, cat_id in categories:
        markdown_filename = f'{feed_dir}/arxiv_org{cat_code}_{timestamp}x.md'
        # content_text = fetch_arxiv_rss(FEED_URL="https://export.arxiv.org/rss/cs.AI", 
        content_text = fetch_arxiv_rss(FEED_URL=f"https://export.arxiv.org/rss/{cat_code}", 
                                    md_file=markdown_filename)

    for cat_code, cat_name, cat_id in categories:
        markdown_filename = f'{feed_dir}/arxiv_org{cat_code}_{timestamp}x.md'
        # content_text = fetch_arxiv_rss(FEED_URL="https://export.arxiv.org/rss/cs.AI", 
        content_text = fetch_arxiv_rss(FEED_URL=f"https://export.arxiv.org/rss/{cat_code}", 
                                    md_file=markdown_filename)
        prompt_text = 'For each article, keep the full title, write a 1-2 sentence summary focusing on objective, method, and key findings, and clearly indicate whether the study appears to be high-impact based on novelty or significance.'
        markdown_filename = f'{feed_dir}/arxiv_summary{cat_code}_{timestamp}x.md'
        markdown_filename_pdf = f'{feed_dir}/arxiv_summary{cat_code}_{timestamp}x.pdf'
        iteration_num=3
        ask_deepseek(prompt_text, content_text, 
                    markdown_filename, markdown_filename_pdf, 
                    iteration_num=iteration_num)
    ###############################################

    ###############################################
    # pubmed
    markdown_filename = f'{feed_dir}/pubmed_org_{timestamp}x.md'
    content_text = fetch_pubmed_rss(FEED_URL="https://pubmed.ncbi.nlm.nih.gov/rss/search/1xePBFBNvSI9gdrM9tn-Tt7zKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=100&utm_campaign=pubmed-2&fc=20250724004604",
                                    md_file=markdown_filename)
    prompt_text = 'For each article, keep the full title, write a 1-2 sentence summary focusing on objective, method, and key findings, and clearly indicate whether the study appears to be high-impact based on novelty or significance.'
    markdown_filename = f'{feed_dir}/pubmed_summary_{timestamp}x.md'
    markdown_filename_pdf = f'{feed_dir}/pubmed_summary_{timestamp}x.pdf'
    iteration_num=3
    ask_deepseek(prompt_text, content_text, 
                 markdown_filename, markdown_filename_pdf, 
                 iteration_num=iteration_num)
    ###############################################
    
    
# print('Waiting for Job to start!')
# schedule.every().hour.at(":15").do(job)
# print('Job for this hour is done!')

job()

schedule.every().day.at("08:15").do(job)
schedule.every().day.at("20:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)