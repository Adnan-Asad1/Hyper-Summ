"""
Reorganize notebook structure:
1. TextRank (Sequential, Parallel, Comparison)
2. TF-IDF (Sequential, Parallel, Comparison)
3. Final Technique Comparison
4. Updated Charts

This script will reorder cells in the notebook
"""

import json

def reorganize_notebook():
    """Reorganize cells in proper order"""
    
    print("Loading project.ipynb...")
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cells = notebook['cells']
    
    # Categorize cells
    setup_cells = []
    textrank_cells = []
    tfidf_cells = []
    comparison_cells = []
    chart_cells = []
    other_cells = []
    
    print("Categorizing cells...")
    for i, cell in enumerate(cells):
        source = ''.join(cell.get('source', []))
        
        # Setup cells (first few cells)
        if i < 6 or 'import' in source[:100] or 'Dataset' in source or 'def preprocess_text' in source or 'def calculate_dynamic_summary_length' in source:
            setup_cells.append(cell)
        # TextRank cells
        elif 'TextRank' in source or 'textrank' in source.lower():
            textrank_cells.append(cell)
        # TF-IDF cells
        elif 'TF-IDF' in source or 'TFIDF' in source or 'tfidf' in source.lower():
            tfidf_cells.append(cell)
        # Comparison cells
        elif 'COMPARATIVE' in source or 'Technique Comparison' in source or 'technique_comparison' in source:
            comparison_cells.append(cell)
        # Chart cells
        elif 'plt.subplots' in source or 'Performance Comparison' in source:
            chart_cells.append(cell)
        else:
            other_cells.append(cell)
    
    print(f"Found {len(setup_cells)} setup cells")
    print(f"Found {len(textrank_cells)} TextRank cells")
    print(f"Found {len(tfidf_cells)} TF-IDF cells")
    print(f"Found {len(comparison_cells)} comparison cells")
    print(f"Found {len(chart_cells)} chart cells")
    print(f"Found {len(other_cells)} other cells")
    
    # Create new cell order
    new_cells = []
    
    # 1. Setup cells
    new_cells.extend(setup_cells)
    
    # 2. TextRank cells
    new_cells.extend(textrank_cells)
    
    # Add TextRank comparison cell if not exists
    has_textrank_comparison = any('TextRank Sequential vs Parallel' in ''.join(c.get('source', [])) for c in textrank_cells)
    if not has_textrank_comparison:
        print("Adding TextRank comparison cell...")
        new_cells.append(create_textrank_comparison_cell())
    
    # 3. TF-IDF cells
    new_cells.extend(tfidf_cells)
    
    # Add TF-IDF comparison cell if not exists
    has_tfidf_comparison = any('TF-IDF Sequential vs Parallel' in ''.join(c.get('source', [])) for c in tfidf_cells)
    if not has_tfidf_comparison:
        print("Adding TF-IDF comparison cell...")
        new_cells.append(create_tfidf_comparison_cell())
    
    # 4. Final comparison cells
    new_cells.extend(comparison_cells)
    
    # 5. Chart cells
    new_cells.extend(chart_cells)
    
    # 6. Other cells
    new_cells.extend(other_cells)
    
    # Update notebook
    notebook['cells'] = new_cells
    
    print(f"\nNew cell order: {len(new_cells)} total cells")
    print("Saving reorganized notebook...")
    
    with open('project.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("\n[OK] Notebook reorganized successfully!")
    print("\nNew structure:")
    print("1. Setup (imports, dataset, utilities)")
    print("2. TextRank (Sequential, Parallel, Comparison)")
    print("3. TF-IDF (Sequential, Parallel, Comparison)")
    print("4. Final Technique Comparison")
    print("5. Performance Charts")

def create_textrank_comparison_cell():
    """Create TextRank Sequential vs Parallel comparison cell"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_seq_vs_par",
        "metadata": {},
        "outputs": [],
        "source": [
            "# TextRank: Sequential vs Parallel Comparison\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TEXTRANK: SEQUENTIAL VS PARALLEL COMPARISON\")\n",
            "print(f\"{'='*80}\")\n",
            "\n",
            "textrank_speedup = textrank_seq_summary['total_time'] / textrank_par_summary['total_time']\n",
            "print(f\"\\nSpeedup: {textrank_speedup:.2f}x\")\n",
            "print(f\"Time saved: {textrank_seq_summary['total_time'] - textrank_par_summary['total_time']:.4f} seconds\")\n",
            "print(f\"Parallel efficiency: {(textrank_speedup / cpu_count()) * 100:.2f}%\")\n",
            "print(f\"Number of CPU cores used: {cpu_count()}\")"
        ]
    }

def create_tfidf_comparison_cell():
    """Create TF-IDF Sequential vs Parallel comparison cell"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "tfidf_seq_vs_par",
        "metadata": {},
        "outputs": [],
        "source": [
            "# TF-IDF: Sequential vs Parallel Comparison\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"TF-IDF: SEQUENTIAL VS PARALLEL COMPARISON\")\n",
            "print(f\"{'='*80}\")\n",
            "\n",
            "tfidf_speedup = seq_summary['total_time'] / par_summary['total_time']\n",
            "print(f\"\\nSpeedup: {tfidf_speedup:.2f}x\")\n",
            "print(f\"Time saved: {seq_summary['total_time'] - par_summary['total_time']:.4f} seconds\")\n",
            "print(f\"Parallel efficiency: {(tfidf_speedup / cpu_count()) * 100:.2f}%\")\n",
            "print(f\"Number of CPU cores used: {cpu_count()}\")"
        ]
    }

if __name__ == "__main__":
    reorganize_notebook()
