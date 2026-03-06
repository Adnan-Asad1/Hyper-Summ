import json
import sys

def add_summary_display_cells():
    """
    Add cells to display original text, summary, and their lengths
    for both TextRank and TF-IDF techniques
    """
    
    # Load the notebook
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cells = notebook['cells']
    
    # First, remove any existing display cells to avoid duplicates
    display_ids = [
        'textrank_seq_display_title', 'textrank_seq_display',
        'textrank_par_display_title', 'textrank_par_display',
        'tfidf_seq_display_title', 'tfidf_seq_display',
        'tfidf_par_display_title', 'tfidf_par_display'
    ]
    
    cells = [cell for cell in cells if cell.get('id') not in display_ids]
    
    # Find the index after TextRank Sequential execution
    textrank_seq_exec_idx = None
    textrank_par_exec_idx = None
    tfidf_seq_exec_idx = None
    tfidf_par_exec_idx = None
    
    for i, cell in enumerate(cells):
        if cell.get('id') == 'textrank_seq_exec':
            textrank_seq_exec_idx = i
        elif cell.get('id') == 'textrank_par_exec':
            textrank_par_exec_idx = i
        elif cell.get('id') == 'tfidf_seq_exec':
            tfidf_seq_exec_idx = i
        elif cell.get('id') == 'tfidf_par_exec':
            tfidf_par_exec_idx = i
    
    # Create display cells for TextRank Sequential
    textrank_seq_display_title = {
        "cell_type": "markdown",
        "id": "textrank_seq_display_title",
        "metadata": {},
        "source": [
            "### 3.3 TextRank Sequential - Sample Summary Display"
        ]
    }
    
    textrank_seq_display_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_seq_display",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Display sample summaries from TextRank Sequential\n",
            "print(\"=\"*80)\n",
            "print(\"TEXTRANK SEQUENTIAL - SAMPLE SUMMARIES\")\n",
            "print(\"=\"*80)\n",
            "print()\n",
            "\n",
            "# Show first 3 articles as examples\n",
            "textrank_seq_summarizer_display = SequentialTextRankSummarizer()\n",
            "\n",
            "for idx in range(min(3, len(test_articles))):\n",
            "    article = test_articles[idx]\n",
            "    summary, metrics = textrank_seq_summarizer_display.summarize(article)\n",
            "    \n",
            "    print(f\"\\nArticle {idx + 1}:\")\n",
            "    print(\"-\" * 80)\n",
            "    print(f\"Original Text ({len(article)} characters, {len(article.split())} words):\")\n",
            "    print(article)\n",
            "    print()\n",
            "    print(f\"Summary ({len(summary)} characters, {len(summary.split())} words):\")\n",
            "    print(summary)\n",
            "    print()\n",
            "    print(f\"Compression: {len(article.split())} words -> {len(summary.split())} words\")\n",
            "    print(f\"Compression Ratio: {metrics['compression_ratio']:.2f}%\")\n",
            "    print(\"=\" * 80)\n"
        ]
    }
    
    # Create display cells for TextRank Parallel
    textrank_par_display_title = {
        "cell_type": "markdown",
        "id": "textrank_par_display_title",
        "metadata": {},
        "source": [
            "### 3.4 TextRank Parallel - Sample Summary Display"
        ]
    }
    
    textrank_par_display_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_par_display",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Display sample summaries from TextRank Parallel\n",
            "print(\"=\"*80)\n",
            "print(\"TEXTRANK PARALLEL - SAMPLE SUMMARIES\")\n",
            "print(\"=\"*80)\n",
            "print()\n",
            "\n",
            "# Show first 3 articles as examples\n",
            "textrank_par_summarizer_display = ParallelTextRankSummarizer()\n",
            "\n",
            "for idx in range(min(3, len(test_articles))):\n",
            "    article = test_articles[idx]\n",
            "    summary, metrics = textrank_par_summarizer_display.summarize(article)\n",
            "    \n",
            "    print(f\"\\nArticle {idx + 1}:\")\n",
            "    print(\"-\" * 80)\n",
            "    print(f\"Original Text ({len(article)} characters, {len(article.split())} words):\")\n",
            "    print(article)\n",
            "    print()\n",
            "    print(f\"Summary ({len(summary)} characters, {len(summary.split())} words):\")\n",
            "    print(summary)\n",
            "    print()\n",
            "    print(f\"Compression: {len(article.split())} words -> {len(summary.split())} words\")\n",
            "    print(f\"Compression Ratio: {metrics['compression_ratio']:.2f}%\")\n",
            "    print(\"=\" * 80)\n"
        ]
    }
    
    # Create display cells for TF-IDF Sequential
    tfidf_seq_display_title = {
        "cell_type": "markdown",
        "id": "tfidf_seq_display_title",
        "metadata": {},
        "source": [
            "### 4.3 TF-IDF Sequential - Sample Summary Display"
        ]
    }
    
    tfidf_seq_display_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "tfidf_seq_display",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Display sample summaries from TF-IDF Sequential\n",
            "print(\"=\"*80)\n",
            "print(\"TF-IDF SEQUENTIAL - SAMPLE SUMMARIES\")\n",
            "print(\"=\"*80)\n",
            "print()\n",
            "\n",
            "# Show first 3 articles as examples\n",
            "tfidf_seq_summarizer_display = SequentialTFIDFSummarizer()\n",
            "\n",
            "for idx in range(min(3, len(test_articles))):\n",
            "    article = test_articles[idx]\n",
            "    summary, metrics = tfidf_seq_summarizer_display.summarize(article)\n",
            "    \n",
            "    print(f\"\\nArticle {idx + 1}:\")\n",
            "    print(\"-\" * 80)\n",
            "    print(f\"Original Text ({len(article)} characters, {len(article.split())} words):\")\n",
            "    print(article)\n",
            "    print()\n",
            "    print(f\"Summary ({len(summary)} characters, {len(summary.split())} words):\")\n",
            "    print(summary)\n",
            "    print()\n",
            "    print(f\"Compression: {len(article.split())} words -> {len(summary.split())} words\")\n",
            "    print(f\"Compression Ratio: {metrics['compression_ratio']:.2f}%\")\n",
            "    print(\"=\" * 80)\n"
        ]
    }
    
    # Create display cells for TF-IDF Parallel
    tfidf_par_display_title = {
        "cell_type": "markdown",
        "id": "tfidf_par_display_title",
        "metadata": {},
        "source": [
            "### 4.4 TF-IDF Parallel - Sample Summary Display"
        ]
    }
    
    tfidf_par_display_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "tfidf_par_display",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Display sample summaries from TF-IDF Parallel\n",
            "print(\"=\"*80)\n",
            "print(\"TF-IDF PARALLEL - SAMPLE SUMMARIES\")\n",
            "print(\"=\"*80)\n",
            "print()\n",
            "\n",
            "# Show first 3 articles as examples\n",
            "tfidf_par_summarizer_display = ParallelTFIDFSummarizer()\n",
            "\n",
            "for idx in range(min(3, len(test_articles))):\n",
            "    article = test_articles[idx]\n",
            "    summary, metrics = tfidf_par_summarizer_display.summarize(article)\n",
            "    \n",
            "    print(f\"\\nArticle {idx + 1}:\")\n",
            "    print(\"-\" * 80)\n",
            "    print(f\"Original Text ({len(article)} characters, {len(article.split())} words):\")\n",
            "    print(article)\n",
            "    print()\n",
            "    print(f\"Summary ({len(summary)} characters, {len(summary.split())} words):\")\n",
            "    print(summary)\n",
            "    print()\n",
            "    print(f\"Compression: {len(article.split())} words -> {len(summary.split())} words\")\n",
            "    print(f\"Compression Ratio: {metrics['compression_ratio']:.2f}%\")\n",
            "    print(\"=\" * 80)\n"
        ]
    }
    
    # Insert cells at appropriate positions
    new_cells = []
    
    for i, cell in enumerate(cells):
        new_cells.append(cell)
        
        # After TextRank Sequential execution
        if i == textrank_seq_exec_idx:
            new_cells.append(textrank_seq_display_title)
            new_cells.append(textrank_seq_display_code)
        
        # After TextRank Parallel execution
        elif i == textrank_par_exec_idx:
            new_cells.append(textrank_par_display_title)
            new_cells.append(textrank_par_display_code)
        
        # After TF-IDF Sequential execution
        elif tfidf_seq_exec_idx and i == tfidf_seq_exec_idx:
            new_cells.append(tfidf_seq_display_title)
            new_cells.append(tfidf_seq_display_code)
        
        # After TF-IDF Parallel execution
        elif tfidf_par_exec_idx and i == tfidf_par_exec_idx:
            new_cells.append(tfidf_par_display_title)
            new_cells.append(tfidf_par_display_code)
    
    notebook['cells'] = new_cells
    
    # Save the updated notebook
    with open('project.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("SUCCESS: Successfully added summary display cells to the notebook!")
    print(f"  - Total cells after update: {len(new_cells)}")
    print(f"  - Added TextRank Sequential display after cell {textrank_seq_exec_idx}")
    print(f"  - Added TextRank Parallel display after cell {textrank_par_exec_idx}")
    if tfidf_seq_exec_idx:
        print(f"  - Added TF-IDF Sequential display after cell {tfidf_seq_exec_idx}")
    if tfidf_par_exec_idx:
        print(f"  - Added TF-IDF Parallel display after cell {tfidf_par_exec_idx}")

if __name__ == "__main__":
    try:
        add_summary_display_cells()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
