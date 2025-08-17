from universal_rss_fetcher2 import UniversalRSSFetcher
import datetime

fetcher = UniversalRSSFetcher()
result = fetcher.fetch_universal_rss(
    "https://feedx.net/rss/bbc.xml",
    source_type="news",
    md_file=f"./tmp/news_bbc1_{datetime.date.today().strftime('%Y%m%d')}.md"
)
print(result)