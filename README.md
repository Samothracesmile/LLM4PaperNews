# LLM4PaperNews

LLM4PaperNews fetches paper listings from arXiv and PubMed RSS feeds and automatically summarizes them with a local LLM. The tool saves both the generated summaries and original listings as Markdown files and can convert them to PDF.

## Features

### RSS fetching
- `universal_rss_fetcher2.py` automatically detects feed types (arXiv, PubMed, Wiley, etc.) and provides flexible field extraction with plain‑text, Markdown, or PDF output.

### Summarization
- `paper_reader_kernel.py` interacts with a local LLM via `ollama run deepseek-r1:70b` to create concise summaries.
- Generated Markdown can be converted to PDF using `md2pdf`.

### Scheduling
- `paper_feeder.py` runs twice a day (08:15 and 20:15) to fetch new feeds and produce summaries.

### Output
- Files are written to the `feeds/` directory; sample output is included in the repository.

## Installation

```bash
pip install feedparser PyMuPDF fpdf schedule beautifulsoup4
```

Ensure that `ollama` (with the e.g. `deepseek-r1:70b` model) and `md2pdf` are installed and available in your `PATH`.

## Usage

### Scheduled run

```bash
python paper_feeder.py
```

This fetches new RSS entries, summarizes them with the LLM, and saves results in the `feeds/` folder.

Edit the `feed_dir` path in `paper_feeder.py` to store output elsewhere. See `example_usage.py` and [`README_universal_rss.md`](README_universal_rss.md) for additional examples.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

