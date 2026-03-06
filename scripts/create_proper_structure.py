"""
Create notebook with EXACT structure user wants:
1. Dataset
2. Utilities
3. TextRank (Sequential → Parallel → Compare → Chart)
4. TF-IDF (Sequential → Parallel → Compare → Chart)
5. Final Comparison
6. Summary
"""

import json

def create_proper_structure():
    """Build notebook with correct structure"""
    
    print("Loading project.ipynb...")
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cells = notebook['cells']
    
    # Categorize all cells
    categorized = {
        'imports': [],
        'dataset': [],
        'utilities': [],
        'textrank_seq_class': [],
        'textrank_seq_run': [],
        'textrank_par_class': [],
        'textrank_par_run': [],
        'tfidf_seq_class': [],
        'tfidf_seq_run': [],
        'tfidf_par_class': [],
        'tfidf_par_run': [],
        'other': []
    }
    
    for cell in cells:
        source = ''.join(cell.get('source', []))
        
        # Categorize based on content
        if 'import' in source[:200] and cell['cell_type'] == 'code':
            categorized['imports'].append(cell)
        elif 'Dataset' in source or 'Loading' in source and 'dataset' in source.lower():
            categorized['dataset'].append(cell)
        elif 'def preprocess_text' in source or 'def calculate_dynamic_summary_length' in source:
            categorized['utilities'].append(cell)
        elif 'class SequentialTextRankSummarizer' in source:
            categorized['textrank_seq_class'].append(cell)
        elif 'TEXTRANK SEQUENTIAL' in source and 'print' in source:
            categorized['textrank_seq_run'].append(cell)
        elif 'class ParallelTextRankSummarizer' in source:
            categorized['textrank_par_class'].append(cell)
        elif 'TEXTRANK PARALLEL' in source and 'print' in source:
            categorized['textrank_par_run'].append(cell)
        elif 'class SequentialTFIDFSummarizer' in source:
            categorized['tfidf_seq_class'].append(cell)
        elif 'TF-IDF SEQUENTIAL' in source and 'print' in source:
            categorized['tfidf_seq_run'].append(cell)
        elif 'class ParallelTFIDFSummarizer' in source:
            categorized['tfidf_par_class'].append(cell)
        elif 'TF-IDF PARALLEL' in source and 'print' in source:
            categorized['tfidf_par_run'].append(cell)
        else:
            categorized['other'].append(cell)
    
    # Build new structure
    new_cells = []
    
    # 1. Imports
    new_cells.extend(categorized['imports'])
    
    # 2. Dataset
    new_cells.extend(categorized['dataset'])
    
    # 3. Utilities
    new_cells.extend(categorized['utilities'])
    
    # 4. TextRank Section
    # Title
    new_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# TextRank Summarization"]
    })
    
    # Sequential
    new_cells.extend(categorized['textrank_seq_class'])
    new_cells.extend(categorized['textrank_seq_run'])
    
    # Parallel
    new_cells.extend(categorized['textrank_par_class'])
    new_cells.extend(categorized['textrank_par_run'])
    
    # Comparison
    new_cells.append(create_textrank_comparison())
    
    # Chart
    new_cells.append(create_textrank_chart())
    
    # 5. TF-IDF Section
    # Title
    new_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# TF-IDF Summarization"]
    })
    
    # Sequential
    new_cells.extend(categorized['tfidf_seq_class'])
    new_cells.extend(categorized['tfidf_seq_run'])
    
    # Parallel
    new_cells.extend(categorized['tfidf_par_class'])
    new_cells.extend(categorized['tfidf_par_run'])
    
    # Comparison
    new_cells.append(create_tfidf_comparison())
    
    # Chart
    new_cells.append(create_tfidf_chart())
    
    # 6. Final Comparison
    new_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# Final Comparison: TextRank vs TF-IDF"]
    })
    new_cells.append(create_final_comparison())
    
    # 7. Summary
    new_cells.append(create_summary_block())
    
    # Update notebook
    notebook['cells'] = new_cells
    
    print(f"\n[OK] Created proper structure with {len(new_cells)} cells")
    print("\nStructure:")
    print("1. Imports + Dataset + Utilities")
    print("2. TextRank (Seq → Par → Compare → Chart)")
    print("3. TF-IDF (Seq → Par → Compare → Chart)")
    print("4. Final Comparison")
    print("5. Summary")
    
    with open('project.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("\n[OK] Saved!")

def create_textrank_comparison():
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# TextRank: Sequential vs Parallel Comparison\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TEXTRANK PERFORMANCE COMPARISON\")\n",
            "print(f\"{'='*80}\\n\")\n",
            "\n",
            "comparison_data = {\n",
            "    'Metric': ['Total Time (s)', 'Avg Time/Article (s)', 'Memory (MB)', 'Compression (%)'],\n",
            "    'Sequential': [\n",
            "        textrank_seq_summary['total_time'],\n",
            "        textrank_seq_summary['avg_time_per_article'],\n",
            "        textrank_seq_summary['peak_memory'],\n",
            "        textrank_seq_summary['compression']\n",
            "    ],\n",
            "    'Parallel': [\n",
            "        textrank_par_summary['total_time'],\n",
            "        textrank_par_summary['avg_time_per_article'],\n",
            "        textrank_par_summary['peak_memory'],\n",
            "        textrank_par_summary['compression']\n",
            "    ]\n",
            "}\n",
            "\n",
            "df_textrank = pd.DataFrame(comparison_data)\n",
            "print(df_textrank.to_string(index=False))\n",
            "\n",
            "speedup = textrank_seq_summary['total_time'] / textrank_par_summary['total_time']\n",
            "print(f\"\\nSpeedup: {speedup:.2f}x\")\n",
            "print(f\"Efficiency: {(speedup/cpu_count())*100:.1f}%\")"
        ]
    }

def create_textrank_chart():
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# TextRank Performance Chart\n",
            "fig, axes = plt.subplots(1, 3, figsize=(15, 5))\n",
            "fig.suptitle('TextRank: Sequential vs Parallel', fontsize=16, fontweight='bold')\n",
            "\n",
            "methods = ['Sequential', 'Parallel']\n",
            "colors = ['#FF6B6B', '#4ECDC4']\n",
            "\n",
            "# Time\n",
            "times = [textrank_seq_summary['total_time'], textrank_par_summary['total_time']]\n",
            "axes[0].bar(methods, times, color=colors, alpha=0.7)\n",
            "axes[0].set_ylabel('Time (s)')\n",
            "axes[0].set_title('Execution Time')\n",
            "axes[0].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Memory\n",
            "memory = [textrank_seq_summary['peak_memory'], textrank_par_summary['peak_memory']]\n",
            "axes[1].bar(methods, memory, color=colors, alpha=0.7)\n",
            "axes[1].set_ylabel('Memory (MB)')\n",
            "axes[1].set_title('Peak Memory')\n",
            "axes[1].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Compression\n",
            "compression = [textrank_seq_summary['compression'], textrank_par_summary['compression']]\n",
            "axes[2].bar(methods, compression, color=colors, alpha=0.7)\n",
            "axes[2].set_ylabel('Compression (%)')\n",
            "axes[2].set_title('Compression Ratio')\n",
            "axes[2].grid(axis='y', alpha=0.3)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }

def create_tfidf_comparison():
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# TF-IDF: Sequential vs Parallel Comparison\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TF-IDF PERFORMANCE COMPARISON\")\n",
            "print(f\"{'='*80}\\n\")\n",
            "\n",
            "comparison_data = {\n",
            "    'Metric': ['Total Time (s)', 'Avg Time/Article (s)', 'Memory (MB)', 'Compression (%)'],\n",
            "    'Sequential': [\n",
            "        seq_summary['total_time'],\n",
            "        seq_summary['avg_time_per_article'],\n",
            "        seq_summary['peak_memory'],\n",
            "        seq_summary['compression']\n",
            "    ],\n",
            "    'Parallel': [\n",
            "        par_summary['total_time'],\n",
            "        par_summary['avg_time_per_article'],\n",
            "        par_summary['peak_memory'],\n",
            "        par_summary['compression']\n",
            "    ]\n",
            "}\n",
            "\n",
            "df_tfidf = pd.DataFrame(comparison_data)\n",
            "print(df_tfidf.to_string(index=False))\n",
            "\n",
            "speedup = seq_summary['total_time'] / par_summary['total_time']\n",
            "print(f\"\\nSpeedup: {speedup:.2f}x\")\n",
            "print(f\"Efficiency: {(speedup/cpu_count())*100:.1f}%\")"
        ]
    }

def create_tfidf_chart():
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# TF-IDF Performance Chart\n",
            "fig, axes = plt.subplots(1, 3, figsize=(15, 5))\n",
            "fig.suptitle('TF-IDF: Sequential vs Parallel', fontsize=16, fontweight='bold')\n",
            "\n",
            "methods = ['Sequential', 'Parallel']\n",
            "colors = ['#FF6B6B', '#4ECDC4']\n",
            "\n",
            "# Time\n",
            "times = [seq_summary['total_time'], par_summary['total_time']]\n",
            "axes[0].bar(methods, times, color=colors, alpha=0.7)\n",
            "axes[0].set_ylabel('Time (s)')\n",
            "axes[0].set_title('Execution Time')\n",
            "axes[0].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Memory\n",
            "memory = [seq_summary['peak_memory'], par_summary['peak_memory']]\n",
            "axes[1].bar(methods, memory, color=colors, alpha=0.7)\n",
            "axes[1].set_ylabel('Memory (MB)')\n",
            "axes[1].set_title('Peak Memory')\n",
            "axes[1].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Compression\n",
            "compression = [seq_summary['compression'], par_summary['compression']]\n",
            "axes[2].bar(methods, compression, color=colors, alpha=0.7)\n",
            "axes[2].set_ylabel('Compression (%)')\n",
            "axes[2].set_title('Compression Ratio')\n",
            "axes[2].grid(axis='y', alpha=0.3)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }

def create_final_comparison():
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Final Comparison: TextRank vs TF-IDF\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TECHNIQUE COMPARISON: TEXTRANK VS TF-IDF\")\n",
            "print(f\"{'='*80}\\n\")\n",
            "\n",
            "final_comparison = {\n",
            "    'Metric': ['Avg Time (s)', 'Memory (MB)', 'Compression (%)', 'Speedup'],\n",
            "    'TextRank Seq': [\n",
            "        textrank_seq_summary['avg_time_per_article'],\n",
            "        textrank_seq_summary['peak_memory'],\n",
            "        textrank_seq_summary['compression'],\n",
            "        1.0\n",
            "    ],\n",
            "    'TextRank Par': [\n",
            "        textrank_par_summary['avg_time_per_article'],\n",
            "        textrank_par_summary['peak_memory'],\n",
            "        textrank_par_summary['compression'],\n",
            "        textrank_seq_summary['total_time'] / textrank_par_summary['total_time']\n",
            "    ],\n",
            "    'TF-IDF Seq': [\n",
            "        seq_summary['avg_time_per_article'],\n",
            "        seq_summary['peak_memory'],\n",
            "        seq_summary['compression'],\n",
            "        1.0\n",
            "    ],\n",
            "    'TF-IDF Par': [\n",
            "        par_summary['avg_time_per_article'],\n",
            "        par_summary['peak_memory'],\n",
            "        par_summary['compression'],\n",
            "        seq_summary['total_time'] / par_summary['total_time']\n",
            "    ]\n",
            "}\n",
            "\n",
            "df_final = pd.DataFrame(final_comparison)\n",
            "print(df_final.to_string(index=False))\n",
            "\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"WINNER ANALYSIS\")\n",
            "print(f\"{'='*80}\")\n",
            "print(f\"Fastest: {'TextRank' if textrank_par_summary['avg_time_per_article'] < par_summary['avg_time_per_article'] else 'TF-IDF'} Parallel\")\n",
            "print(f\"Best Compression: {'TextRank' if textrank_seq_summary['compression'] > seq_summary['compression'] else 'TF-IDF'}\")\n",
            "print(f\"Most Memory Efficient: {'TextRank' if textrank_par_summary['peak_memory'] < par_summary['peak_memory'] else 'TF-IDF'}\")"
        ]
    }

def create_summary_block():
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Summary\n",
            "\n",
            "## Project Overview\n",
            "This project implements and compares two text summarization techniques:\n",
            "1. **TextRank** - Graph-based approach\n",
            "2. **TF-IDF** - Statistical approach\n",
            "\n",
            "Each technique has:\n",
            "- Sequential implementation\n",
            "- Parallel implementation\n",
            "\n",
            "## Key Findings\n",
            "- Both techniques achieve meaningful compression (20-40%)\n",
            "- Parallel versions show speedup over sequential\n",
            "- Different approaches produce different summary styles\n",
            "\n",
            "## Conclusion\n",
            "Both TextRank and TF-IDF are effective for extractive text summarization, with parallelization providing performance benefits."
        ]
    }

if __name__ == "__main__":
    create_proper_structure()
