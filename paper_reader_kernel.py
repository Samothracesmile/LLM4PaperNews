DEBUG = False  # Set to True to enable debug printouts

"""Utility helpers for reading scientific papers, querying the DeepSeek model, and exporting markdown/PDF summaries."""
import fitz
import subprocess
import os
from fpdf import FPDF
import textwrap
import re
import shlex

# Extract text from a PDF file, up to max_pages
# Debug: Print PDF path and page count

def extract_text_from_pdf(pdf_path, max_pages=50):
    """Return concatenated text from the first *max_pages* pages of *pdf_path*."""
    if DEBUG:
        print(f"[DEBUG] Extracting text from: {pdf_path}, max_pages={max_pages}")
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(len(doc), max_pages)):
        page = doc[page_num]
        text += page.get_text()
    if DEBUG:
        print(f"[DEBUG] Extracted {len(text)} characters from PDF.")
    return text

# Extract text after </think> tag from LLM output
def extract_post_think_text(full_text):
    if DEBUG:
        print(f"[DEBUG] Extracting post-think text.")
    parts = full_text.split("</think>")
    return parts[1].strip() if len(parts) > 1 else full_text

# Query DeepSeek model via Ollama subprocess
# Debug: Print prompt length and context lengthS
def query_deepseek(prompt_text, context_text, llm_model="deepseek-r1:70b"):
    if DEBUG:
        print(f"[DEBUG] Querying DeepSeek: prompt length={len(prompt_text)}, context length={len(context_text)}")
    full_prompt = f"{prompt_text}\n\nHere is the content:\n{context_text}"
    process = subprocess.run(
        ["ollama", "run", llm_model],  
        input=full_prompt,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if process.returncode != 0:
        print(f"[ERROR] DeepSeek execution failed: {process.stderr}")
        raise RuntimeError(f"DeepSeek execution failed:\n{process.stderr}")
    if DEBUG:
        print(f"[DEBUG] DeepSeek output length: {len(process.stdout.strip())}")
    return process.stdout.strip()

# Safely run shell commands with arguments

def run_shell_command(command, *args):
    """Safely run *command* with each argument shell-escaped."""
    safe_args = [shlex.quote(arg) for arg in args]
    cmd_str = f"{command} {' '.join(safe_args)}"
    if DEBUG:
        print(f"[DEBUG] Running shell command: {cmd_str}")
    try:
        subprocess.run(cmd_str, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")

# Main workflow: Query DeepSeek multiple times, merge results, save markdown and PDF

def ask_deepseek(prompt_text, content_text, markdown_filename, markdown_filename_pdf, llm_model="deepseek-r1:70b", llm_model_merge="deepseek-r1:70b", iteration_num=3):
    if DEBUG:
        print(f"[DEBUG] ask_deepseek: markdown_filename={markdown_filename}, iteration_num={iteration_num}")
    if not os.path.exists(markdown_filename):
        all_text = ''
        for ver_idx in range(iteration_num):
            if DEBUG:
                print(f'[DEBUG] In prompt iteration {ver_idx} ...')
            answer = query_deepseek(prompt_text, content_text, llm_model=llm_model)
            main_text = extract_post_think_text(answer)
            all_text = all_text + f'results {ver_idx}:' + main_text
        answer = query_deepseek('Merge all result to one!', all_text,  llm_model=llm_model_merge)
        main_text = extract_post_think_text(answer)
        final_text = main_text
        with open(markdown_filename, "w", encoding="utf-8") as f:
            f.write(final_text)
        print(f"✅ Summary saved as Markdown: {markdown_filename}")
    run_shell_command("md2pdf", markdown_filename, markdown_filename_pdf)