import feedparser
import datetime
import smtplib
from email.mime.text import MIMEText
from paper_reader_kernel import run_shell_command


def fetch_feed(url):
    """Fetch and parse RSS feed from given URL."""
    return feedparser.parse(url)

def parse_entries(feed):
    """Extract paper info from feed object."""
    papers = []
    for entry in feed.entries:
        title = entry.title
        authors = ", ".join(author.name for author in entry.authors) if hasattr(entry, 'authors') else entry.author if hasattr(entry, 'author') else "N/A"
        summary = entry.summary if hasattr(entry, 'summary') else ""
        link = entry.link
        papers.append({"title": title, "authors": authors, "summary": summary, "link": link})
    return papers

def save_as_markdown(papers, file_path):
    """Save paper list to Markdown file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# arXiv cs.AI Latest Papers ({len(papers)} total)\n\n")
        f.write(f"Date: {datetime.date.today()}\n\n")
        for p in papers:
            f.write(f"## {p['title']}\n")
            f.write(f"**Authors:** {p['authors']}\n\n")
            f.write(f"**Abstract:** {p['summary']}\n\n")
            f.write(f"[View Paper]({p['link']})\n\n")
    print(f"Markdown saved to: {file_path}")

def save_as_html(papers, file_path):
    """Save paper list to HTML file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><meta charset='UTF-8'><title>arXiv cs.AI Papers</title></head><body>\n")
        f.write(f"<h1>arXiv cs.AI Latest Papers ({len(papers)})</h1>\n")
        f.write(f"<p>Date: {datetime.date.today()}</p>\n")
        for p in papers:
            f.write(f"<h2>{p['title']}</h2>\n")
            f.write(f"<p><strong>Authors:</strong> {p['authors']}</p>\n")
            f.write(f"<p><strong>Abstract:</strong> {p['summary']}</p>\n")
            f.write(f"<p><a href='{p['link']}'>View Paper</a></p>\n")
            f.write("<hr>\n")
        f.write("</body></html>")
    print(f"HTML saved to: {file_path}")


def send_email(papers, smtp_server, port, sender_email, sender_password, receiver_email):
    """Send paper list as an email."""
    html_content = "<h1>Today's arXiv cs.AI Papers</h1>"
    for p in papers:
        html_content += f"<h2>{p['title']}</h2><p><b>Authors:</b> {p['authors']}</p><p><b>Abstract:</b> {p['summary']}</p><p><a href='{p['link']}'>View Paper</a></p><hr>"
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['Subject'] = "Daily arXiv cs.AI Update"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    print(f"Email sent to: {receiver_email}")

def print_to_console(papers):
    """Print paper list to console."""
    print(f"=== arXiv cs.AI Today's Papers: {len(papers)} ===")
    for p in papers:
        print(f"\nTitle: {p['title']}\nAuthors: {p['authors']}\nAbstract: {p['summary']}\nLink: {p['link']}\n")


def format_pubmed_entries(papers):
    """将 PubMed RSS entries 转换为纯文本格式"""
    formatted = []
    for i, entry in enumerate(papers):
        text = (
            f"[{i}] Title: {entry['title']}\n"
            f"Summary: {entry['summary']}\n"
            f"Link: {entry['link']}\n"
        )
        formatted.append(text)
    return "\n".join(formatted)


def fetch_arxiv_rss(FEED_URL="https://export.arxiv.org/rss/cs.AI", md_file=None):
    feed = fetch_feed(FEED_URL)
    papers = parse_entries(feed)
    
    # today = datetime.date.today().strftime("%Y%m%d")
    if md_file is not None:
        # md_file = f"arxiv_csai_{today}.md"
        # pdf_file = f"arxiv_csai_{today}.pdf"
        pdf_file = md_file.replace('.md', '.pdf')
        save_as_markdown(papers, md_file)

        run_shell_command("md2pdf", md_file, pdf_file)
    
    return format_pubmed_entries(papers)
        
    # Uncomment to enable email sending
    # send_email(papers, "smtp.example.com", 465, "you@example.com", "yourpassword", "receiver@example.com")
