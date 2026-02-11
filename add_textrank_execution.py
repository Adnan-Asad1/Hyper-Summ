"""
Add execution cells for TextRank and comparison with TF-IDF
"""

import json

def create_execution_cells():
    """Create cells to run TextRank and compare techniques"""
    
    cells = []
    
    # Cell 1: Run TextRank Sequential
    cells.append({
        "cell_type": "markdown",
        "id": "textrank_seq_run_title",
        "metadata": {},
        "source": [
            "## Run TextRank Sequential Summarization"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_seq_run",
        "metadata": {},
        "outputs": [],
        "source": [
            "print(\"=\"*80)\n",
            "print(\"TEXTRANK SEQUENTIAL SUMMARIZATION\")\n",
            "print(\"=\"*80)\n",
            "\n",
            "textrank_seq_summarizer = SequentialTextRankSummarizer()\n",
            "textrank_seq_results = []\n",
            "\n",
            "print(f\"\\nProcessing {len(test_articles)} articles with TextRank Sequential...\")\n",
            "start_textrank_seq = time.perf_counter()\n",
            "\n",
            "for i, article in enumerate(test_articles):\n",
            "    summary, metrics = textrank_seq_summarizer.summarize(article)\n",
            "    textrank_seq_results.append(metrics)\n",
            "    print(f\"  Processed: {i + 1}/{len(test_articles)} articles - Time: {metrics['execution_time']:.4f}s\")\n",
            "\n",
            "end_textrank_seq = time.perf_counter()\n",
            "total_textrank_seq_time = end_textrank_seq - start_textrank_seq\n",
            "\n",
            "# Aggregate metrics\n",
            "textrank_seq_metrics_df = pd.DataFrame(textrank_seq_results)\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TEXTRANK SEQUENTIAL RESULTS SUMMARY\")\n",
            "print(f\"{'='*80}\")\n",
            "print(f\"Total execution time: {total_textrank_seq_time:.4f} seconds\")\n",
            "print(f\"Average time per article: {textrank_seq_metrics_df['execution_time'].mean():.4f} seconds\")\n",
            "print(f\"Total memory used: {textrank_seq_metrics_df['memory_used_mb'].sum():.2f} MB\")\n",
            "print(f\"Average memory per article: {textrank_seq_metrics_df['memory_used_mb'].mean():.2f} MB\")\n",
            "print(f\"Peak memory: {textrank_seq_metrics_df['peak_memory_mb'].max():.2f} MB\")\n",
            "print(f\"Average compression ratio: {textrank_seq_metrics_df['compression_ratio'].mean():.2f}%\")\n",
            "print(f\"Average summary length: {textrank_seq_metrics_df['summary_sentences'].mean():.1f} sentences\")\n",
            "\n",
            "# Store for comparison\n",
            "textrank_seq_summary = {\n",
            "    'total_time': total_textrank_seq_time,\n",
            "    'avg_time_per_article': textrank_seq_metrics_df['execution_time'].mean(),\n",
            "    'total_memory': textrank_seq_metrics_df['memory_used_mb'].sum(),\n",
            "    'peak_memory': textrank_seq_metrics_df['peak_memory_mb'].max(),\n",
            "    'compression': textrank_seq_metrics_df['compression_ratio'].mean()\n",
            "}"
        ]
    })
    
    # Cell 2: Run TextRank Parallel
    cells.append({
        "cell_type": "markdown",
        "id": "textrank_par_run_title",
        "metadata": {},
        "source": [
            "## Run TextRank Parallel Summarization"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_par_run",
        "metadata": {},
        "outputs": [],
        "source": [
            "print(\"\\n\" + \"=\"*80)\n",
            "print(\"TEXTRANK PARALLEL SUMMARIZATION\")\n",
            "print(\"=\"*80)\n",
            "\n",
            "textrank_par_summarizer = ParallelTextRankSummarizer(num_processes=cpu_count())\n",
            "textrank_par_results = []\n",
            "\n",
            "print(f\"\\nProcessing {len(test_articles)} articles with TextRank Parallel...\")\n",
            "start_textrank_par = time.perf_counter()\n",
            "\n",
            "for i, article in enumerate(test_articles):\n",
            "    summary, metrics = textrank_par_summarizer.summarize(article)\n",
            "    textrank_par_results.append(metrics)\n",
            "    print(f\"  Processed: {i + 1}/{len(test_articles)} articles - Time: {metrics['execution_time']:.4f}s\")\n",
            "\n",
            "end_textrank_par = time.perf_counter()\n",
            "total_textrank_par_time = end_textrank_par - start_textrank_par\n",
            "\n",
            "# Aggregate metrics\n",
            "textrank_par_metrics_df = pd.DataFrame(textrank_par_results)\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TEXTRANK PARALLEL RESULTS SUMMARY\")\n",
            "print(f\"{'='*80}\")\n",
            "print(f\"Total execution time: {total_textrank_par_time:.4f} seconds\")\n",
            "print(f\"Average time per article: {textrank_par_metrics_df['execution_time'].mean():.4f} seconds\")\n",
            "print(f\"Total memory used: {textrank_par_metrics_df['memory_used_mb'].sum():.2f} MB\")\n",
            "print(f\"Average memory per article: {textrank_par_metrics_df['memory_used_mb'].mean():.2f} MB\")\n",
            "print(f\"Peak memory: {textrank_par_metrics_df['peak_memory_mb'].max():.2f} MB\")\n",
            "print(f\"Average compression ratio: {textrank_par_metrics_df['compression_ratio'].mean():.2f}%\")\n",
            "print(f\"Average summary length: {textrank_par_metrics_df['summary_sentences'].mean():.1f} sentences\")\n",
            "print(f\"Average chunks per article: {textrank_par_metrics_df['num_chunks'].mean():.1f}\")\n",
            "\n",
            "# Store for comparison\n",
            "textrank_par_summary = {\n",
            "    'total_time': total_textrank_par_time,\n",
            "    'avg_time_per_article': textrank_par_metrics_df['execution_time'].mean(),\n",
            "    'total_memory': textrank_par_metrics_df['memory_used_mb'].sum(),\n",
            "    'peak_memory': textrank_par_metrics_df['peak_memory_mb'].max(),\n",
            "    'compression': textrank_par_metrics_df['compression_ratio'].mean()\n",
            "}"
        ]
    })
    
    # Cell 3: Technique Comparison
    cells.append({
        "cell_type": "markdown",
        "id": "technique_comparison_title",
        "metadata": {},
        "source": [
            "## Technique Comparison: TF-IDF vs TextRank"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "id": "technique_comparison",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create comprehensive comparison\n",
            "technique_comparison_data = {\n",
            "    'Metric': [\n",
            "        'Total Execution Time (s)',\n",
            "        'Avg Time Per Article (s)',\n",
            "        'Total Memory Used (MB)',\n",
            "        'Peak Memory (MB)',\n",
            "        'Compression Ratio (%)'\n",
            "    ],\n",
            "    'TF-IDF Sequential': [\n",
            "        seq_summary['total_time'],\n",
            "        seq_summary['avg_time_per_article'],\n",
            "        seq_summary['total_memory'],\n",
            "        seq_summary['peak_memory'],\n",
            "        seq_summary['compression']\n",
            "    ],\n",
            "    'TF-IDF Parallel': [\n",
            "        par_summary['total_time'],\n",
            "        par_summary['avg_time_per_article'],\n",
            "        par_summary['total_memory'],\n",
            "        par_summary['peak_memory'],\n",
            "        par_summary['compression']\n",
            "    ],\n",
            "    'TextRank Sequential': [\n",
            "        textrank_seq_summary['total_time'],\n",
            "        textrank_seq_summary['avg_time_per_article'],\n",
            "        textrank_seq_summary['total_memory'],\n",
            "        textrank_seq_summary['peak_memory'],\n",
            "        textrank_seq_summary['compression']\n",
            "    ],\n",
            "    'TextRank Parallel': [\n",
            "        textrank_par_summary['total_time'],\n",
            "        textrank_par_summary['avg_time_per_article'],\n",
            "        textrank_par_summary['total_memory'],\n",
            "        textrank_par_summary['peak_memory'],\n",
            "        textrank_par_summary['compression']\n",
            "    ]\n",
            "}\n",
            "\n",
            "technique_comparison_df = pd.DataFrame(technique_comparison_data)\n",
            "\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"COMPREHENSIVE TECHNIQUE COMPARISON\")\n",
            "print(f\"{'='*80}\\n\")\n",
            "print(technique_comparison_df.to_string(index=False))\n",
            "\n",
            "# Calculate speedups\n",
            "tfidf_speedup = seq_summary['total_time'] / par_summary['total_time']\n",
            "textrank_speedup = textrank_seq_summary['total_time'] / textrank_par_summary['total_time']\n",
            "\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"SPEEDUP ANALYSIS\")\n",
            "print(f\"{'='*80}\")\n",
            "print(f\"TF-IDF Speedup (Sequential vs Parallel): {tfidf_speedup:.2f}x\")\n",
            "print(f\"TextRank Speedup (Sequential vs Parallel): {textrank_speedup:.2f}x\")\n",
            "print(f\"\\nTechnique Comparison (Sequential):\")\n",
            "print(f\"  TF-IDF vs TextRank time ratio: {seq_summary['total_time'] / textrank_seq_summary['total_time']:.2f}x\")\n",
            "print(f\"\\nTechnique Comparison (Parallel):\")\n",
            "print(f\"  TF-IDF vs TextRank time ratio: {par_summary['total_time'] / textrank_par_summary['total_time']:.2f}x\")"
        ]
    })
    
    return cells

def main():
    print("Loading project.ipynb...")
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    print("Creating execution and comparison cells...")
    new_cells = create_execution_cells()
    
    # Find where to insert (after TextRank Parallel class)
    insert_index = None
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code' and 'source' in cell:
            source = ''.join(cell['source'])
            if 'ParallelTextRankSummarizer class defined' in source:
                insert_index = i + 1
                break
    
    if insert_index is None:
        print("Could not find insertion point, adding at end...")
        insert_index = len(notebook['cells'])
    
    print(f"Inserting {len(new_cells)} new cells at position {insert_index}...")
    
    # Insert new cells
    for i, cell in enumerate(new_cells):
        notebook['cells'].insert(insert_index + i, cell)
    
    print("Saving updated notebook...")
    with open('project.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("\n[OK] TextRank execution cells added successfully!")
    print(f"\nAdded {len(new_cells)} new cells:")
    print("1. Run TextRank Sequential (title + code)")
    print("2. Run TextRank Parallel (title + code)")
    print("3. Technique Comparison (title + code)")
    print("\nTotal new cells added to notebook: 10")
    print("  - 4 class definition cells")
    print("  - 6 execution/comparison cells")

if __name__ == "__main__":
    main()
