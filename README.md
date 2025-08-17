# LLM4PaperNews

LLM4PaperNews fetches paper listings from arXiv and PubMed RSS feeds and automatically summarizes them using a local LLM. Generated summaries and original listings are saved in Markdown and converted to PDF.

## Features

- **RSS Fetching**
  - `fetch_arxiv_rss.py` downloads the latest `cs.AI` entries from arXiv.
  - `fetch_pubmed_rss.py` downloads PubMed search results using a predefined RSS URL.
- **Summarization**
  - `paper_reader_kernel.py` interacts with a local LLM via `ollama run deepseek-r1:70b` to create short summaries.
  - Markdown files are converted to PDF using `md2pdf`.
- **Scheduling**
  - `paper_feeder.py` runs twice a day (08:15 and 20:15) to fetch new feeds and produce summaries.
- **Output**
  - Files are written to the `feeds/` directory; sample output is included in the repository.

## Requirements

- Python 3
- Packages: `feedparser`, `PyMuPDF` (`fitz`), `fpdf`, `schedule`
- External commands: `ollama` (with the `deepseek-r1:70b` model) and `md2pdf`

Install Python dependencies with:

```bash
pip install feedparser PyMuPDF fpdf schedule
```

Ensure `ollama` and `md2pdf` are available in your `PATH`.

## Usage

1. Run `paper_feeder.py` to start the scheduled job:

```bash
python paper_feeder.py
```

The script fetches new RSS entries, summarizes them using the LLM, and saves results in the `feeds/` folder.

2. To fetch a feed once without scheduling, call `fetch_arxiv_rss()` or `fetch_pubmed_rss()` from the corresponding scripts.

Edit the `feed_dir` path in `paper_feeder.py` if you want to store output elsewhere.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

