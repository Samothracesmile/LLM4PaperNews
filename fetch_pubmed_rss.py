import feedparser
import datetime
from paper_reader_kernel import run_shell_command

def fetch_rss(url):
    """Fetch the RSS feed from the given URL."""
    return feedparser.parse(url)

def parse_entries(feed):
    """Extract relevant fields from feed entries."""
    entries = []
    for e in feed.entries:
        title = e.title
        pub_date = e.get('published', '')
        summary = e.get('summary', '')
        link = e.link
        entries.append({
            'title': title,
            'pub_date': pub_date,
            'summary': summary,
            'link': link
        })
    return entries

def format_markdown(entries):
    """Format entries as a Markdown string."""
    output = f"Date: {datetime.date.today()}\n\n"
    for e in entries:
        output += f"## {e['title']}\n"
        output += f"**Publication Date:** {e['pub_date']}\n\n"
        output += f"**Summary:** {e['summary']}\n\n"
        output += f"[Link]({e['link']})\n\n"
    return output

def format_pubmed_entries(entries):
    """将 PubMed RSS entries 转换为纯文本格式"""
    formatted = []
    for i, entry in enumerate(entries):
        text = (
            f"[{i}] Title: {entry['title']}\n"
            f"Date: {entry['pub_date']}\n"
            f"Summary: {entry['summary']}\n"
            f"Link: {entry['link']}\n"
        )
        formatted.append(text)
    return "\n".join(formatted)

def save_markdown(entries, dest):
    """Save entries to a Markdown file."""
    content = format_markdown(entries)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(content)

def fetch_pubmed_rss(FEED_URL = "https://pubmed.ncbi.nlm.nih.gov/rss/search/1xePBFBNvSI9gdrM9tn-Tt7zKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=100&utm_campaign=pubmed-2&fc=20250724004604",
                     md_file=None):
    
    feed = fetch_rss(FEED_URL)
    entries = parse_entries(feed)

    # save origial rss
    # today = datetime.date.today().strftime("%Y%m%d")
    if md_file is not None:
        # md_file = f"pubmed_{today}.md"
        # pdf_file = f"pubmed_{today}.pdf"
        pdf_file = md_file.replace('.md', '.pdf')
        save_markdown(entries, md_file)
        run_shell_command("md2pdf", md_file, pdf_file)
    
    return format_pubmed_entries(entries)
