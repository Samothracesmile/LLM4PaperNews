import feedparser
import datetime
from bs4 import BeautifulSoup
from paper_reader_kernel import run_shell_command
from typing import Dict, List, Optional, Callable, Any


class UniversalRSSFetcher:
    """通用RSS抓取器，支持自适应不同RSS源的结构"""
    
    def __init__(self):
        # 预定义的RSS源配置
        self.source_configs = {
            'pubmed': {
                'fields': {
                    'title': 'title',
                    'pub_date': 'published',
                    'summary': 'summary',
                    'link': 'link'
                },
                'feed_name': 'PubMed'
            },
            'arxiv': {
                'fields': {
                    'title': 'title',
                    'authors': self._extract_arxiv_authors,
                    'summary': 'summary',
                    'link': 'link'
                },
                'feed_name': 'arXiv'
            },
            'wiley': {
                'fields': {
                    'title': 'title',
                    'authors': 'dc_creator',
                    'pub_date': 'published',
                    'doi': 'dc_identifier',
                    'link': 'link',
                    'abstract': self._extract_wiley_abstract
                },
                'feed_name': 'Wiley'
            }
        }
    
    def _extract_arxiv_authors(self, entry) -> str:
        """提取arXiv作者信息"""
        if hasattr(entry, 'authors'):
            return ", ".join(author.name for author in entry.authors)
        elif hasattr(entry, 'author'):
            return entry.author
        return "N/A"
    
    def _extract_wiley_abstract(self, entry) -> str:
        """提取Wiley摘要信息"""
        content_html = entry.get('content', [{}])[0].get('value', '')
        if content_html:
            soup = BeautifulSoup(content_html, 'html.parser')
            ps = soup.find_all('p')
            if ps:
                return "\n\n".join(p.get_text(strip=True) for p in ps).strip()
            return soup.get_text(strip=True)
        return getattr(entry, 'summary', '')
    
    def fetch_rss(self, url: str) -> Any:
        """获取RSS feed"""
        return feedparser.parse(url)
    
    def parse_entries(self, feed: Any, config: Dict) -> List[Dict]:
        """根据配置解析RSS条目"""
        entries = []
        fields_config = config.get('fields', {})
        
        for entry in feed.entries:
            parsed_entry = {}
            
            for field_name, field_source in fields_config.items():
                if callable(field_source):
                    # 如果是函数，调用函数提取
                    parsed_entry[field_name] = field_source(entry)
                elif isinstance(field_source, str):
                    # 如果是字符串，直接获取属性
                    parsed_entry[field_name] = getattr(entry, field_source, '')
                else:
                    parsed_entry[field_name] = ''
            
            entries.append(parsed_entry)
        
        return entries
    
    def auto_detect_source(self, feed: Any) -> str:
        """自动检测RSS源类型"""
        if not feed.entries:
            return 'generic'
        
        entry = feed.entries[0]
        
        # 检测arXiv
        if hasattr(entry, 'authors') or 'arxiv.org' in getattr(entry, 'link', ''):
            return 'arxiv'
        
        # 检测Wiley
        if hasattr(entry, 'dc_creator') or hasattr(entry, 'dc_identifier'):
            return 'wiley'
        
        # 检测PubMed
        if 'pubmed.ncbi.nlm.nih.gov' in getattr(entry, 'link', ''):
            return 'pubmed'
        
        return 'generic'
    
    def get_generic_config(self, feed: Any) -> Dict:
        """为未知RSS源生成通用配置"""
        if not feed.entries:
            return {'fields': {}, 'feed_name': 'Generic RSS'}
        
        entry = feed.entries[0]
        fields = {}
        
        # 尝试常见字段
        common_fields = ['title', 'link', 'summary', 'published', 'author', 'description']
        for field in common_fields:
            if hasattr(entry, field):
                fields[field] = field
        
        return {
            'fields': fields,
            'feed_name': 'Generic RSS'
        }
    
    def format_entries_text(self, entries: List[Dict]) -> str:
        """将条目格式化为纯文本"""
        formatted = []
        for i, entry in enumerate(entries):
            text_parts = [f"[{i}] Title: {entry.get('title', 'N/A')}"]
            
            # 动态添加其他字段
            for key, value in entry.items():
                if key != 'title' and value:
                    text_parts.append(f"{key.title()}: {value}")
            
            formatted.append("\n".join(text_parts))
        
        return "\n\n".join(formatted)
    
    def save_markdown(self, entries: List[Dict], file_path: str, feed_name: str = "RSS Feed"):
        """保存为Markdown格式"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {feed_name} ({len(entries)} entries)\n\n")
            f.write(f"Date: {datetime.date.today()}\n\n")
            
            for entry in entries:
                f.write(f"## {entry.get('title', 'No Title')}\n")
                
                # 动态写入其他字段
                for key, value in entry.items():
                    if key != 'title' and value:
                        f.write(f"**{key.title()}:** {value}\n\n")
                
                if 'link' in entry:
                    f.write(f"[View Article]({entry['link']})\n\n")
        
        print(f"✅ Markdown saved: {file_path}")
    
    def fetch_universal_rss(self, 
                           url: str, 
                           source_type: Optional[str] = None,
                           custom_config: Optional[Dict] = None,
                           md_file: Optional[str] = None) -> str:
        """通用RSS抓取主函数
        
        Args:
            url: RSS URL
            source_type: 指定源类型 ('pubmed', 'arxiv', 'wiley', 'generic')
            custom_config: 自定义配置
            md_file: Markdown输出文件路径
        
        Returns:
            格式化的文本字符串
        """
        # 获取RSS feed
        feed = self.fetch_rss(url)
        
        # 确定配置
        if custom_config:
            config = custom_config
        elif source_type and source_type in self.source_configs:
            config = self.source_configs[source_type]
        else:
            # 自动检测
            detected_type = self.auto_detect_source(feed)
            if detected_type in self.source_configs:
                config = self.source_configs[detected_type]
            else:
                config = self.get_generic_config(feed)
        
        # 解析条目
        entries = self.parse_entries(feed, config)
        
        # 保存Markdown文件
        if md_file:
            feed_name = config.get('feed_name', 'RSS Feed')
            self.save_markdown(entries, md_file, feed_name)
            
            # 生成PDF
            pdf_file = md_file.replace('.md', '.pdf')
            run_shell_command("md2pdf", md_file, pdf_file)
        
        # 返回格式化文本
        return self.format_entries_text(entries)
    
    def add_custom_source(self, name: str, config: Dict):
        """添加自定义RSS源配置"""
        self.source_configs[name] = config


# 便捷函数
def fetch_rss_universal(url: str, 
                       source_type: Optional[str] = None,
                       custom_config: Optional[Dict] = None,
                       md_file: Optional[str] = None) -> str:
    """便捷的通用RSS抓取函数"""
    fetcher = UniversalRSSFetcher()
    return fetcher.fetch_universal_rss(url, source_type, custom_config, md_file)


# 兼容性函数，保持与原有脚本的接口一致
def fetch_pubmed_rss(FEED_URL: str = "https://pubmed.ncbi.nlm.nih.gov/rss/search/1xePBFBNvSI9gdrM9tn-Tt7zKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=100&utm_campaign=pubmed-2&fc=20250724004604",
                     md_file: Optional[str] = None) -> str:
    return fetch_rss_universal(FEED_URL, 'pubmed', md_file=md_file)


def fetch_arxiv_rss(FEED_URL: str = "https://export.arxiv.org/rss/cs.AI", 
                    md_file: Optional[str] = None) -> str:
    return fetch_rss_universal(FEED_URL, 'arxiv', md_file=md_file)


def fetch_wiley_feed(FEED_URL: str = "https://onlinelibrary.wiley.com/feed/14679299/most-recent",
                     md_file: Optional[str] = None,
                     **kwargs) -> str:
    return fetch_rss_universal(FEED_URL, 'wiley', md_file=md_file)


if __name__ == "__main__":
    # 使用示例
    fetcher = UniversalRSSFetcher()
    
    # 示例1: 自动检测RSS源类型
    result1 = fetcher.fetch_universal_rss(
        "https://export.arxiv.org/rss/cs.AI",
        md_file="arxiv_auto.md"
    )
    
    # 示例2: 指定RSS源类型
    result2 = fetcher.fetch_universal_rss(
        "https://pubmed.ncbi.nlm.nih.gov/rss/search/...",
        source_type="pubmed",
        md_file="pubmed_specified.md"
    )
    
    # 示例3: 使用自定义配置
    custom_config = {
        'fields': {
            'title': 'title',
            'date': 'published',
            'content': 'summary'
        },
        'feed_name': 'Custom RSS Source'
    }
    
    result3 = fetcher.fetch_universal_rss(
        "https://example.com/rss",
        custom_config=custom_config,
        md_file="custom_rss.md"
    )
    
    print("Universal RSS Fetcher ready!")