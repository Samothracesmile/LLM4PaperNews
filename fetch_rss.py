import feedparser
import datetime
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from paper_reader_kernel import run_shell_command


def fetch_feed(url):
    return feedparser.parse(url)


def extract_abstract(content_html):
    soup = BeautifulSoup(content_html, 'html.parser')
    ps = soup.find_all('p')
    if ps:
        return "\n\n".join(p.get_text(strip=True) for p in ps).strip()
    return soup.get_text(strip=True)


def parse_wiley_entries(feed):
    papers = []
    for entry in feed.entries:
        title = getattr(entry, 'title', 'No Title')
        authors = getattr(entry, 'dc_creator', 'N/A')
        pub_date = getattr(entry, 'published', 'Unknown Date')
        doi = getattr(entry, 'dc_identifier', 'N/A')
        link = getattr(entry, 'link', '#')

        content_html = entry.get('content', [{}])[0].get('value', '')
        abstract = extract_abstract(content_html) or getattr(entry, 'summary', '')

        papers.append({
            "title": title,
            "authors": authors,
            "pub_date": pub_date,
            "doi": doi,
            "link": link,
            "abstract": abstract
        })
    return papers


def save_as_markdown(papers, file_path, feed_name="Wiley Feed"):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {feed_name} ({len(papers)} articles)\n\n")
        f.write(f"Date: {datetime.date.today()}\n\n")
        for p in papers:
            f.write(f"## {p['title']}\n")
            f.write(f"**Authors:** {p['authors']}\n\n")
            f.write(f"**Date:** {p['pub_date']}\n\n")
            f.write(f"**Abstract:** {p['abstract']}\n\n")
            f.write(f"**DOI:** {p['doi']}\n\n")
            f.write(f"[View Article]({p['link']})\n\n")
    print(f"✅ Markdown saved: {file_path}")


def save_as_html(papers, file_path, feed_name="Wiley Feed"):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"<html><head><meta charset='utf-8'><title>{feed_name}</title></head><body>\n")
        f.write(f"<h1>{feed_name} ({len(papers)} articles)</h1>\n")
        f.write(f"<p>Date: {datetime.date.today()}</p>\n")
        for p in papers:
            f.write(f"<h2>{p['title']}</h2>\n")
            f.write(f"<p><strong>Authors:</strong> {p['authors']}</p>\n")
            f.write(f"<p><strong>Date:</strong> {p['pub_date']}</p>\n")
            f.write(f"<p><strong>Abstract:</strong> {p['abstract']}</p>\n")
            f.write(f"<p><strong>DOI:</strong> {p['doi']}</p>\n")
            f.write(f"<p><a href='{p['link']}'>View Article</a></p>\n<hr>\n")
        f.write("</body></html>")
    print(f"✅ HTML saved: {file_path}")


def send_email(papers, smtp_server, port, sender_email, sender_password, receiver_email, feed_name="Wiley Feed"):
    html = f"<h1>{feed_name} Articles</h1>"
    for p in papers:
        html += (
            f"<h2>{p['title']}</h2>"
            f"<p><b>Authors:</b> {p['authors']}</p>"
            f"<p><b>Date:</b> {p['pub_date']}</p>"
            f"<p><b>Abstract:</b> {p['abstract']}</p>"
            f"<p><b>DOI:</b> {p['doi']}</p>"
            f"<p><a href='{p['link']}'>View Article</a></p><hr>"
        )
    msg = MIMEText(html, 'html', 'utf-8')
    msg['Subject'] = f"{feed_name} Digest"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    print(f"📧 Email sent to {receiver_email}")


def print_to_console(papers):
    for i, p in enumerate(papers, 1):
        print(f"[{i}] {p['title']}")
        print(f"Authors: {p['authors']}")
        print(f"Date: {p['pub_date']}")
        print(f"DOI: {p['doi']}")
        print(f"Abstract: {p['abstract']}")
        print(f"Link: {p['link']}")
        print("-" * 60)


def fetch_wiley_feed(
    FEED_URL="https://onlinelibrary.wiley.com/feed/14679299/most-recent",
    md_file=None,
    html_file=None,
    feed_name="Wiley: Public Administration",
    send_as_email=False,
    email_conf=None,
    to_console=True
):
    feed = fetch_feed(FEED_URL)
    papers = parse_wiley_entries(feed)

    if md_file:
        save_as_markdown(papers, md_file, feed_name)
        pdf_file = md_file.replace('.md', '.pdf')
        run_shell_command("md2pdf", md_file, pdf_file)

    if html_file:
        save_as_html(papers, html_file, feed_name)

    if send_as_email and email_conf:
        send_email(papers, **email_conf, feed_name=feed_name)

    if to_console:
        print_to_console(papers)

    return papers