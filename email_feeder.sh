#!/bin/bash
# vim: set filetype=sh :
# vim: syntax=sh autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 textwidth=220
export LANG=C.UTF-8

# =========================
# arXiv Weekly Digest Script
# Author: (Your Name)
# Version: v03
# Last Modified: 2025-07-25
# =========================

# Output file initialization
OUTFILE="/ifs/loni/faculty/shi/spectrum/yxia/tmp/arxiv.txt"
DATE=$(date +'%Y-%m-%d')
echo "$DATE" > "$OUTFILE"

# =========================
# Helper Function: fetch_and_format
# =========================
fetch_and_format() {
    local URL="$1"
    local TMPFILE="$2"
    local SECTION_TITLE="$3"

    curl -s "$URL" > "$TMPFILE"

    grep -E '<h3>|<span class="descriptor">Title:</span> |href="/abs/' "$TMPFILE" > /ifs/loni/faculty/shi/spectrum/yxia/tmp/tmp_filtered.txt

    sed -r -i '
        s/<h3>/\n========================================\n/
        s/<\/h3>/\n========================================/
        s/<span class="descriptor">Title:<\/span> /• /g
        s/.*"(\/abs.*?)".*/    https:\/\/arxiv.org\1/
    ' /ifs/loni/faculty/shi/spectrum/yxia/tmp/tmp_filtered.txt

    sed -i '
        s/".*$//
        s/^<.*//g
    ' /ifs/loni/faculty/shi/spectrum/yxia/tmp/tmp_filtered.txt

    printf "\n===============================================================================" >> "$OUTFILE"
    printf "\n===============================================================================" >> "$OUTFILE"
    printf "\n$SECTION_TITLE [$DATE]" >> "$OUTFILE"
    printf "\n===============================================================================" >> "$OUTFILE"
    printf "\n===============================================================================\n" >> "$OUTFILE"

    tac /ifs/loni/faculty/shi/spectrum/yxia/tmp/tmp_filtered.txt >> "$OUTFILE"
}

# =========================
# Main Sections
# =========================
fetch_and_format \
    'https://arxiv.org/list/cs.AI/pastweek?skip=0&show=200' \
    /ifs/loni/faculty/shi/spectrum/yxia/tmp/cs_ai.txt \
    '[1/5] ARTIFICIAL INTELLIGENCE'

fetch_and_format \
    'https://arxiv.org/list/cs.CL/pastweek?skip=0&show=100' \
    /ifs/loni/faculty/shi/spectrum/yxia/tmp/cs_cl.txt \
    '[2/5] COMPUTATION AND LANGUAGE'

fetch_and_format \
    'https://arxiv.org/list/cs.IR/recent' \
    /ifs/loni/faculty/shi/spectrum/yxia/tmp/cs_ir.txt \
    '[3/5] INFORMATION RETRIEVAL'

fetch_and_format \
    'https://arxiv.org/list/cs.LG/pastweek?skip=0&show=150' \
    /ifs/loni/faculty/shi/spectrum/yxia/tmp/cs_lg.txt \
    '[4/5] MACHINE LEARNING'

fetch_and_format \
    'https://arxiv.org/list/stat.ML/pastweek?skip=0&show=50' \
    /ifs/loni/faculty/shi/spectrum/yxia/tmp/stat_ml.txt \
    '[5/5] STATISTICS - MACHINE LEARNING'

# =========================
# Send Email
# =========================
# mail -s 'arxiv' mail@VictoriasJourney.com < "$OUTFILE"
mail -s 'arxiv' yihaoxia@outlook.com < "$OUTFILE"

# End of script
