#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用RSS抓取器使用示例
演示如何使用UniversalRSSFetcher处理不同类型的RSS源
"""

from universal_rss_fetcher import UniversalRSSFetcher, fetch_rss_universal
import datetime

def example_arxiv_categories():
    """示例1: arXiv多个类别RSS抓取"""
    print("=== 示例1: arXiv多个类别RSS抓取 ===")
    
    fetcher = UniversalRSSFetcher()
    
    # arXiv不同类别的RSS源
    arxiv_categories = {
        'cs.AI': 'https://export.arxiv.org/rss/cs.AI',  # 人工智能
        'cs.LG': 'https://export.arxiv.org/rss/cs.LG',  # 机器学习
        'cs.CV': 'https://export.arxiv.org/rss/cs.CV',  # 计算机视觉
        'cs.CL': 'https://export.arxiv.org/rss/cs.CL',  # 计算语言学
        'cs.IR': 'https://export.arxiv.org/rss/cs.IR',  # 信息检索
        'stat.ML': 'https://export.arxiv.org/rss/stat.ML',  # 统计机器学习
        'q-bio.QM': 'https://export.arxiv.org/rss/q-bio.QM',  # 定量方法
        'physics.med-ph': 'https://export.arxiv.org/rss/physics.med-ph'  # 医学物理
    }
    
    for category, url in arxiv_categories.items():
        print(f"\n正在抓取 arXiv {category} 类别...")
        result = fetcher.fetch_universal_rss(
            url,
            source_type="arxiv",
            md_file=f"arxiv_{category.replace('.', '_')}_{datetime.date.today().strftime('%Y%m%d')}.md"
        )
        print(f"arXiv {category} RSS抓取完成，共{len(result.split('['))-1}篇论文")


def example_pubmed_searches():
    """示例2: PubMed多种搜索RSS抓取"""
    print("\n=== 示例2: PubMed多种搜索RSS抓取 ===")
    
    fetcher = UniversalRSSFetcher()
    
    # PubMed不同搜索主题的RSS源
    pubmed_searches = {
        'machine_learning': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1xePBFBNvSI9gdrM9tn-Tt7zKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=50',
        'deep_learning': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1FAHpokKtVoGHHS9cKWVZZJZKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=50',
        'covid19': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1BcGHHS9cKWVZZJZKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=50',
        'cancer_research': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1CcGHHS9cKWVZZJZKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=50',
        'neuroscience': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1DcGHHS9cKWVZZJZKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=50'
    }
    
    for topic, url in pubmed_searches.items():
        print(f"\n正在抓取 PubMed {topic} 主题...")
        result = fetcher.fetch_universal_rss(
            url,
            source_type="pubmed",
            md_file=f"pubmed_{topic}_{datetime.date.today().strftime('%Y%m%d')}.md"
        )
        print(f"PubMed {topic} RSS抓取完成，共{len(result.split('['))-1}篇文章")


def example_wiley_journals():
    """示例3: Wiley多个期刊RSS抓取"""
    print("\n=== 示例3: Wiley多个期刊RSS抓取 ===")
    
    fetcher = UniversalRSSFetcher()
    
    # Wiley不同期刊的RSS源
    wiley_journals = {
        'public_admin': 'https://onlinelibrary.wiley.com/feed/14679299/most-recent',  # Public Administration
        'j_public_admin': 'https://onlinelibrary.wiley.com/feed/15406210/most-recent',  # Journal of Public Administration Research and Theory
        'policy_studies': 'https://onlinelibrary.wiley.com/feed/15411338/most-recent',  # Policy Studies Journal
        'governance': 'https://onlinelibrary.wiley.com/feed/14680491/most-recent',  # Governance
        'public_budgeting': 'https://onlinelibrary.wiley.com/feed/15405850/most-recent',  # Public Budgeting & Finance
        'intl_review': 'https://onlinelibrary.wiley.com/feed/14682346/most-recent',  # International Review of Administrative Sciences
        'admin_society': 'https://onlinelibrary.wiley.com/feed/14679299/most-recent',  # Administration & Society
        'policy_politics': 'https://onlinelibrary.wiley.com/feed/17411130/most-recent'  # Policy & Politics
    }
    
    for journal, url in wiley_journals.items():
        print(f"\n正在抓取 Wiley {journal} 期刊...")
        result = fetcher.fetch_universal_rss(
            url,
            source_type="wiley",
            md_file=f"wiley_{journal}_{datetime.date.today().strftime('%Y%m%d')}.md"
        )
        print(f"Wiley {journal} RSS抓取完成，共{len(result.split('['))-1}篇文章")


def example_nature_journals():
    """示例4: Nature多个子刊RSS抓取"""
    print("\n=== 示例4: Nature多个子刊RSS抓取 ===")
    
    fetcher = UniversalRSSFetcher()
    
    # 添加Nature系列期刊配置
    nature_config = {
        'fields': {
            'title': 'title',
            'authors': lambda entry: getattr(entry, 'author', 'N/A'),
            'pub_date': 'published',
            'summary': 'summary',
            'link': 'link',
            'doi': lambda entry: getattr(entry, 'prism_doi', getattr(entry, 'id', 'N/A'))
        },
        'feed_name': 'Nature Publishing Group'
    }
    
    fetcher.add_custom_source('nature', nature_config)
    
    # Nature系列期刊RSS源
    nature_journals = {
        'nature': 'https://www.nature.com/nature.rss',  # Nature主刊
        'nature_methods': 'https://www.nature.com/nmeth.rss',  # Nature Methods
        'nature_biotechnology': 'https://www.nature.com/nbt.rss',  # Nature Biotechnology
        'nature_medicine': 'https://www.nature.com/nm.rss',  # Nature Medicine
        'nature_neuroscience': 'https://www.nature.com/nn.rss',  # Nature Neuroscience
        'nature_genetics': 'https://www.nature.com/ng.rss',  # Nature Genetics
        'nature_communications': 'https://www.nature.com/ncomms.rss',  # Nature Communications
        'scientific_reports': 'https://www.nature.com/srep.rss',  # Scientific Reports
        'nature_machine_intelligence': 'https://www.nature.com/natmachintell.rss',  # Nature Machine Intelligence
        'nature_computational_science': 'https://www.nature.com/natcomputsci.rss'  # Nature Computational Science
    }
    
    for journal, url in nature_journals.items():
        print(f"\n正在抓取 {journal} 期刊...")
        try:
            result = fetcher.fetch_universal_rss(
                url,
                source_type="nature",
                md_file=f"{journal}_{datetime.date.today().strftime('%Y%m%d')}.md"
            )
            print(f"{journal} RSS抓取完成，共{len(result.split('['))-1}篇文章")
        except Exception as e:
            print(f"{journal} RSS抓取失败: {e}")


def example_mixed_sources():
    """示例5: 混合多种RSS源自动检测"""
    print("\n=== 示例5: 混合多种RSS源自动检测 ===")
    
    fetcher = UniversalRSSFetcher()
    
    # 混合不同类型的RSS源，测试自动检测功能
    mixed_sources = {
        'arxiv_ai': 'https://export.arxiv.org/rss/cs.AI',
        'pubmed_ml': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1xePBFBNvSI9gdrM9tn-Tt7zKhbcCb-LBo0-Af-WHFfgDglsyb/?limit=20',
        'wiley_admin': 'https://onlinelibrary.wiley.com/feed/14679299/most-recent',
        'nature_main': 'https://www.nature.com/nature.rss'
    }
    
    for source_name, url in mixed_sources.items():
        print(f"\n正在自动检测并抓取 {source_name}...")
        try:
            # 不指定source_type，让系统自动检测
            result = fetcher.fetch_universal_rss(
                url,
                md_file=f"auto_{source_name}_{datetime.date.today().strftime('%Y%m%d')}.md"
            )
            detected_type = fetcher.auto_detect_source(fetcher.fetch_rss(url))
            print(f"{source_name} 自动检测为 {detected_type} 类型，抓取完成")
        except Exception as e:
            print(f"{source_name} 抓取失败: {e}")


def example_compatibility():
    """示例6: 与原有脚本的兼容性"""
    print("\n=== 示例6: 兼容性函数 ===")
    
    # 这些函数保持与原有脚本相同的接口
    from universal_rss_fetcher import fetch_pubmed_rss, fetch_arxiv_rss, fetch_wiley_feed
    
    # 使用原有接口
    pubmed_result = fetch_pubmed_rss(
        md_file=f"pubmed_compat_{datetime.date.today().strftime('%Y%m%d')}.md"
    )
    print("PubMed兼容性函数调用完成")
    
    arxiv_result = fetch_arxiv_rss(
        md_file=f"arxiv_compat_{datetime.date.today().strftime('%Y%m%d')}.md"
    )
    print("arXiv兼容性函数调用完成")


if __name__ == "__main__":
    print("通用RSS抓取器使用示例")
    print("=" * 50)
    
    try:
        # 运行所有示例
        example_arxiv_categories()
        example_pubmed_searches()
        example_wiley_journals()
        example_nature_journals()
        example_mixed_sources()
        example_compatibility()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成！")
        print("\n使用说明:")
        print("1. 自动检测: 让系统自动识别RSS源类型")
        print("2. 指定类型: 明确指定RSS源类型 (pubmed/arxiv/wiley/generic)")
        print("3. 自定义配置: 为特殊RSS源定义字段映射")
        print("4. 添加新源: 永久添加新的RSS源配置")
        print("5. 通用处理: 处理任意结构的RSS")
        print("6. 兼容模式: 使用原有脚本的函数接口")
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        print("请确保已安装所需依赖: feedparser, beautifulsoup4")