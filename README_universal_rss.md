# 通用RSS抓取器 (Universal RSS Fetcher)

一个自适应的RSS抓取工具，能够智能识别和处理不同来源的RSS feed，包括PubMed、arXiv、Wiley等学术期刊和任意RSS源。

## 主要特性

### 🔍 自动检测RSS源类型
- 智能识别PubMed、arXiv、Wiley等常见学术RSS源
- 自动应用相应的字段提取规则
- 对未知RSS源提供通用解析方案

### ⚙️ 灵活的配置系统
- 预定义常见RSS源的解析配置
- 支持自定义字段映射和提取函数
- 可动态添加新的RSS源配置

### 📄 多格式输出
- 纯文本格式输出
- Markdown文件生成
- 自动PDF转换（需要md2pdf工具）

### 🔄 向后兼容
- 保持与原有脚本相同的函数接口
- 无缝替换现有的RSS抓取脚本

## 安装依赖

```bash
pip install feedparser beautifulsoup4
```

## 快速开始

### 基本使用

```python
from universal_rss_fetcher import fetch_rss_universal

# 自动检测RSS源类型
result = fetch_rss_universal(
    "https://export.arxiv.org/rss/cs.AI",
    md_file="arxiv_papers.md"
)
print(result)
```

### 指定RSS源类型

```python
# 明确指定为arXiv类型
result = fetch_rss_universal(
    "https://export.arxiv.org/rss/cs.LG",
    source_type="arxiv",
    md_file="arxiv_ml.md"
)
```

### 使用类接口

```python
from universal_rss_fetcher import UniversalRSSFetcher

fetcher = UniversalRSSFetcher()
result = fetcher.fetch_universal_rss(
    "https://pubmed.ncbi.nlm.nih.gov/rss/search/...",
    source_type="pubmed",
    md_file="pubmed_results.md"
)
```

## 支持的RSS源类型

### 1. PubMed (`pubmed`)
- **字段**: title, pub_date, summary, link
- **自动检测**: URL包含`pubmed.ncbi.nlm.nih.gov`

### 2. arXiv (`arxiv`)
- **字段**: title, authors, summary, link
- **自动检测**: URL包含`arxiv.org`或条目包含authors字段
- **特殊处理**: 智能提取作者信息

### 3. Wiley (`wiley`)
- **字段**: title, authors, pub_date, doi, link, abstract
- **自动检测**: 条目包含`dc_creator`或`dc_identifier`字段
- **特殊处理**: HTML内容解析提取摘要

### 4. 通用 (`generic`)
- **字段**: 自动检测常见字段
- **适用**: 任意RSS源

## 高级用法

### 自定义配置

```python
from universal_rss_fetcher import UniversalRSSFetcher

# 定义自定义配置
custom_config = {
    'fields': {
        'title': 'title',
        'publication_date': 'published',
        'abstract': 'summary',
        'url': 'link',
        'category': lambda entry: getattr(entry, 'tags', [{}])[0].get('term', 'N/A')
    },
    'feed_name': 'Custom Academic RSS'
}

fetcher = UniversalRSSFetcher()
result = fetcher.fetch_universal_rss(
    "https://example.com/rss",
    custom_config=custom_config,
    md_file="custom_rss.md"
)
```

### 添加新的RSS源配置

```python
fetcher = UniversalRSSFetcher()

# 添加Nature期刊配置
nature_config = {
    'fields': {
        'title': 'title',
        'authors': lambda entry: getattr(entry, 'author', 'N/A'),
        'pub_date': 'published',
        'summary': 'summary',
        'link': 'link',
        'journal': lambda entry: 'Nature'
    },
    'feed_name': 'Nature Journal'
}

fetcher.add_custom_source('nature', nature_config)

# 使用新配置
result = fetcher.fetch_universal_rss(
    "https://www.nature.com/nature.rss",
    source_type="nature",
    md_file="nature_papers.md"
)
```

## 兼容性函数

为了保持与原有脚本的兼容性，提供了以下函数：

```python
from universal_rss_fetcher import fetch_pubmed_rss, fetch_arxiv_rss, fetch_wiley_feed

# 与原有脚本完全相同的接口
pubmed_result = fetch_pubmed_rss(md_file="pubmed.md")
arxiv_result = fetch_arxiv_rss(md_file="arxiv.md")
wiley_result = fetch_wiley_feed(md_file="wiley.md")
```

## 配置字段说明

### 字段映射类型

1. **字符串映射**: 直接从RSS条目属性获取
   ```python
   'title': 'title'  # 获取entry.title
   ```

2. **函数映射**: 使用自定义函数处理
   ```python
   'authors': lambda entry: ", ".join(author.name for author in entry.authors)
   ```

### 常见字段名

- `title`: 标题
- `authors`: 作者
- `pub_date`: 发布日期
- `summary`/`abstract`: 摘要
- `link`/`url`: 链接
- `doi`: DOI标识符

## 输出格式

### 文本格式
```
[0] Title: Paper Title
Authors: Author1, Author2
Summary: Paper abstract...
Link: https://example.com/paper

[1] Title: Another Paper
...
```

### Markdown格式
```markdown
# RSS Feed (10 entries)

Date: 2025-01-27

## Paper Title
**Authors:** Author1, Author2
**Summary:** Paper abstract...
[View Article](https://example.com/paper)
```

## 错误处理

- RSS获取失败时返回空结果
- 字段缺失时使用默认值或空字符串
- 自定义函数异常时跳过该字段

## 性能优化

- 延迟加载BeautifulSoup（仅在需要时导入）
- 缓存RSS源类型检测结果
- 批量处理RSS条目

## 扩展示例

查看 `example_usage.py` 文件获取完整的使用示例，包括：

1. 自动检测RSS源类型
2. 指定RSS源类型
3. 使用自定义配置
4. 添加新的RSS源配置
5. 处理未知类型的RSS
6. 兼容性函数使用

## 与原有脚本的对比

| 特性 | 原有脚本 | 通用抓取器 |
|------|----------|------------|
| RSS源支持 | 单一源 | 多源自适应 |
| 配置方式 | 硬编码 | 配置驱动 |
| 扩展性 | 需修改代码 | 动态配置 |
| 兼容性 | N/A | 完全兼容 |
| 自动检测 | 无 | 智能检测 |

## 注意事项

1. 确保网络连接正常，能够访问RSS URL
2. 某些RSS源可能需要特殊的User-Agent或认证
3. PDF生成需要安装`md2pdf`工具
4. 大量RSS条目可能影响处理速度

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！