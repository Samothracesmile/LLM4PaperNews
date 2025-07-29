import requests
import re
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

# Set UTF-8 encoding
os.environ['LANG'] = 'C.UTF-8'

# Email configuration (modify these for your SMTP server)
SMTP_SERVER = 'smtp.gmail.com'  # e.g., 'smtp.gmail.com' for Gmail
SMTP_PORT = 587  # e.g., 587 for Gmail TLS, 465 for SSL
SENDER_EMAIL = 'xiasamothrace1@gmail.com'  # Replace with your email
SENDER_PASSWORD = 'Yifan93@Loni..,,'  # Replace with your password or app-specific password
RECIPIENT_EMAIL = 'xiasamothrace@gmail.com'

# File paths
output_file = '/ifs/loni/faculty/shi/spectrum/yxia/tmp/arxiv.txt'
temp_files = {
    'cs.AI': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/awi2eing.txt',
    'cs.CL': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/gei6sihu.txt',
    'cs.IR': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/ahpahn4v.txt',
    'cs.LG': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/ohgai5ni.txt',
    'stat.ML': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/eeb8lae7.txt'
}
processed_files = {
    'cs.AI': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/ai.txt',
    'cs.CL': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/cl.txt',
    'cs.IR': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/ir.txt',
    'cs.LG': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/ml.txt',
    'stat.ML': '/ifs/loni/faculty/shi/spectrum/yxia/tmp/statml.txt'
}

# arXiv URLs for each category
urls = {
    'cs.AI': 'https://arxiv.org/list/cs.AI/pastweek?skip=0&show=200',
    'cs.CL': 'https://arxiv.org/list/cs.CL/pastweek?skip=0&show=100',
    'cs.IR': 'https://arxiv.org/list/cs.IR/recent',
    'cs.LG': 'https://arxiv.org/list/cs.LG/pastweek?skip=0&show=150',
    'stat.ML': 'https://arxiv.org/list/stat.ML/pastweek?skip=0&show=50'
}

# Category names and order
categories = [
    ('cs.AI', 'ARTIFICIAL INTELLIGENCE', 1),
    ('cs.CL', 'COMPUTATION AND LANGUAGE', 2),
    ('cs.IR', 'INFORMATION RETRIEVAL', 3),
    ('cs.LG', 'COMPUTER SCIENCE - MACHINE LEARNING', 4),
    ('stat.ML', 'STATISTICS - MACHINE LEARNING', 5)
]

# Write current date to output file (overwrites if exists)
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"{datetime.now().strftime('%Y-%m-%d')}\n")

# Process each category
for category, category_name, index in categories:
    try:
        # Fetch HTML content
        response = requests.get(urls[category], timeout=10)
        response.raise_for_status()
        with open(temp_files[category], 'w', encoding='utf-8') as f:
            f.write(response.text)

        # Read and filter lines
        with open(temp_files[category], 'r', encoding='utf-8') as f:
            lines = f.readlines()
        filtered_lines = [line for line in lines if re.search(r'<h3>|Title:</span>|href="/abs/', line)]

        # Process lines
        processed_lines = []
        for line in filtered_lines:
            # Replace <h3> with separators
            line = re.sub(r'<h3>', '\n\n========================================\n', line)
            line = re.sub(r'</h3>', '\n========================================', line)
            # Replace title descriptor with bullet
            line = re.sub(r'<span class="descriptor">Title:</span>\s*', '• ', line)
            # Convert relative URLs to full URLs
            line = re.sub(r'.*"(\/abs\/[^"]+)".*', r'https://arxiv.org\1', line)
            # Remove residual HTML and trailing quotes
            line = re.sub(r'".*$', '', line)
            line = re.sub(r'^<.*$', '', line)
            if line.strip():
                processed_lines.append(line)

        # Write processed lines to temp file
        with open(processed_files[category], 'w', encoding='utf-8') as f:
            f.write(''.join(processed_lines))

        # Append to output file in reverse order
        with open(processed_files[category], 'r', encoding='utf-8') as f:
            processed_lines = f.readlines()
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("\n===============================================================================\n")
            f.write("===============================================================================\n")
            f.write(f"[{index}/5] {category_name} [{datetime.now().strftime('%Y-%m-%d')}]\n")
            f.write("===============================================================================\n")
            f.write("===============================================================================\n")
            f.write(''.join(processed_lines[::-1]) + '\n')

    except Exception as e:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\nError processing {category_name}: {str(e)}\n")

# Send email
try:
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = 'arxiv'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    # Connect to SMTP server with TLS
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Enable TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
except Exception as e:
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"\nError sending email: {str(e)}\n")