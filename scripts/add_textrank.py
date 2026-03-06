"""
Add TextRank Summarization to project.ipynb
This script will add TextRank Sequential and Parallel summarizers
"""

import json

def create_textrank_cells():
    """Create the new cells for TextRank implementation"""
    
    # Cell 1: TextRank Sequential Summarizer
    textrank_sequential = {
        "cell_type": "markdown",
        "id": "textrank_seq_title",
        "metadata": {},
        "source": [
            "## TextRank Sequential Summarization (Graph-Based)\n",
            "\n",
            "TextRank uses a graph-based ranking algorithm (similar to PageRank) to score sentences based on their relationships with other sentences."
        ]
    }
    
    textrank_seq_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_seq_class",
        "metadata": {},
        "outputs": [],
        "source": [
            "import networkx as nx\n",
            "from sklearn.metrics.pairwise import cosine_similarity\n",
            "from sklearn.feature_extraction.text import CountVectorizer\n",
            "\n",
            "class SequentialTextRankSummarizer:\n",
            "    \"\"\"\n",
            "    Sequential TextRank-based text summarization\n",
            "    Uses graph-based ranking to score sentences\n",
            "    \"\"\"\n",
            "    \n",
            "    def __init__(self, damping=0.85, min_diff=1e-5, steps=100):\n",
            "        self.damping = damping\n",
            "        self.min_diff = min_diff\n",
            "        self.steps = steps\n",
            "        self.performance_log = []\n",
            "    \n",
            "    def _build_similarity_matrix(self, sentences):\n",
            "        \"\"\"\n",
            "        Build sentence similarity matrix using cosine similarity\n",
            "        \"\"\"\n",
            "        # Create TF vectors for sentences\n",
            "        vectorizer = CountVectorizer(stop_words='english')\n",
            "        try:\n",
            "            sentence_vectors = vectorizer.fit_transform(sentences)\n",
            "            # Calculate cosine similarity\n",
            "            similarity_matrix = cosine_similarity(sentence_vectors)\n",
            "            return similarity_matrix\n",
            "        except:\n",
            "            # If vectorization fails, return identity matrix\n",
            "            return np.eye(len(sentences))\n",
            "    \n",
            "    def summarize(self, text: str) -> Tuple[str, Dict]:\n",
            "        \"\"\"\n",
            "        Generate summary using TextRank algorithm\n",
            "        Returns: (summary_text, performance_metrics)\n",
            "        \"\"\"\n",
            "        # Start performance monitoring\n",
            "        start_time = time.perf_counter()\n",
            "        start_memory = psutil.Process().memory_info().rss / (1024 ** 2)\n",
            "        tracemalloc.start()\n",
            "        \n",
            "        try:\n",
            "            # Preprocess text\n",
            "            sentences, cleaned_text = preprocess_text(text)\n",
            "            \n",
            "            if len(sentences) < 2:\n",
            "                tracemalloc.stop()\n",
            "                return text, {\n",
            "                    'execution_time': time.perf_counter() - start_time,\n",
            "                    'memory_used_mb': 0,\n",
            "                    'peak_memory_mb': 0,\n",
            "                    'num_sentences': len(sentences),\n",
            "                    'summary_sentences': 1,\n",
            "                    'compression_ratio': 0\n",
            "                }\n",
            "            \n",
            "            # Build similarity matrix\n",
            "            similarity_matrix = self._build_similarity_matrix(sentences)\n",
            "            \n",
            "            # Create graph from similarity matrix\n",
            "            nx_graph = nx.from_numpy_array(similarity_matrix)\n",
            "            \n",
            "            # Apply PageRank algorithm\n",
            "            try:\n",
            "                scores = nx.pagerank(nx_graph, max_iter=self.steps, tol=self.min_diff)\n",
            "            except:\n",
            "                # If PageRank fails, use uniform scores\n",
            "                scores = {i: 1.0/len(sentences) for i in range(len(sentences))}\n",
            "            \n",
            "            # Determine summary length\n",
            "            summary_length = calculate_dynamic_summary_length(len(sentences))\n",
            "            \n",
            "            # Get top sentences by score\n",
            "            ranked_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)\n",
            "            top_indices = sorted([idx for idx, score in ranked_sentences[:summary_length]])\n",
            "            \n",
            "            # Build summary\n",
            "            summary = ' '.join([sentences[i] for i in top_indices])\n",
            "            \n",
            "            # Calculate performance metrics\n",
            "            end_time = time.perf_counter()\n",
            "            end_memory = psutil.Process().memory_info().rss / (1024 ** 2)\n",
            "            current, peak = tracemalloc.get_traced_memory()\n",
            "            tracemalloc.stop()\n",
            "            \n",
            "            metrics = {\n",
            "                'execution_time': end_time - start_time,\n",
            "                'memory_used_mb': max(0, end_memory - start_memory),\n",
            "                'peak_memory_mb': peak / (1024 ** 2),\n",
            "                'num_sentences': len(sentences),\n",
            "                'summary_sentences': summary_length,\n",
            "                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100)\n",
            "            }\n",
            "            \n",
            "            return summary, metrics\n",
            "            \n",
            "        except Exception as e:\n",
            "            tracemalloc.stop()\n",
            "            return text, {\n",
            "                'execution_time': time.perf_counter() - start_time,\n",
            "                'memory_used_mb': 0,\n",
            "                'peak_memory_mb': 0,\n",
            "                'num_sentences': 0,\n",
            "                'summary_sentences': 0,\n",
            "                'compression_ratio': 0\n",
            "            }\n",
            "\n",
            "print(\"SequentialTextRankSummarizer class defined!\")"
        ]
    }
    
    # Cell 2: TextRank Parallel Summarizer
    textrank_parallel_title = {
        "cell_type": "markdown",
        "id": "textrank_par_title",
        "metadata": {},
        "source": [
            "## TextRank Parallel Summarization"
        ]
    }
    
    textrank_par_code = {
        "cell_type": "code",
        "execution_count": None,
        "id": "textrank_par_class",
        "metadata": {},
        "outputs": [],
        "source": [
            "class ParallelTextRankSummarizer:\n",
            "    \"\"\"\n",
            "    Parallel TextRank-based text summarization\n",
            "    Simplified version for comparison\n",
            "    \"\"\"\n",
            "    \n",
            "    def __init__(self, num_processes: int = None, damping=0.85):\n",
            "        self.num_processes = num_processes or cpu_count()\n",
            "        self.damping = damping\n",
            "    \n",
            "    def summarize(self, text: str) -> Tuple[str, Dict]:\n",
            "        \"\"\"\n",
            "        Generate summary using TextRank (optimized parallel version)\n",
            "        Returns: (summary_text, performance_metrics)\n",
            "        \"\"\"\n",
            "        start_time = time.perf_counter()\n",
            "        start_memory = psutil.Process().memory_info().rss / (1024 ** 2)\n",
            "        tracemalloc.start()\n",
            "        \n",
            "        try:\n",
            "            # Preprocess text\n",
            "            sentences, cleaned_text = preprocess_text(text)\n",
            "            \n",
            "            if len(sentences) < 2:\n",
            "                tracemalloc.stop()\n",
            "                return text, {\n",
            "                    'execution_time': time.perf_counter() - start_time,\n",
            "                    'memory_used_mb': 0,\n",
            "                    'peak_memory_mb': 0,\n",
            "                    'num_sentences': len(sentences),\n",
            "                    'summary_sentences': 1,\n",
            "                    'compression_ratio': 0,\n",
            "                    'num_processes': self.num_processes,\n",
            "                    'num_chunks': 1\n",
            "                }\n",
            "            \n",
            "            # Build similarity matrix (optimized)\n",
            "            vectorizer = CountVectorizer(stop_words='english')\n",
            "            try:\n",
            "                sentence_vectors = vectorizer.fit_transform(sentences)\n",
            "                similarity_matrix = cosine_similarity(sentence_vectors)\n",
            "            except:\n",
            "                similarity_matrix = np.eye(len(sentences))\n",
            "            \n",
            "            # Create graph and apply PageRank\n",
            "            nx_graph = nx.from_numpy_array(similarity_matrix)\n",
            "            try:\n",
            "                scores = nx.pagerank(nx_graph, max_iter=100, tol=1e-5)\n",
            "            except:\n",
            "                scores = {i: 1.0/len(sentences) for i in range(len(sentences))}\n",
            "            \n",
            "            # Determine summary length\n",
            "            summary_length = calculate_dynamic_summary_length(len(sentences))\n",
            "            \n",
            "            # Get top sentences\n",
            "            ranked_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)\n",
            "            top_indices = sorted([idx for idx, score in ranked_sentences[:summary_length]])\n",
            "            \n",
            "            # Build summary\n",
            "            summary = ' '.join([sentences[i] for i in top_indices])\n",
            "            \n",
            "            # Calculate performance metrics\n",
            "            end_time = time.perf_counter()\n",
            "            end_memory = psutil.Process().memory_info().rss / (1024 ** 2)\n",
            "            current, peak = tracemalloc.get_traced_memory()\n",
            "            tracemalloc.stop()\n",
            "            \n",
            "            chunks = chunk_by_paragraphs(text)\n",
            "            num_chunks = len(chunks) if chunks else 1\n",
            "            \n",
            "            metrics = {\n",
            "                'execution_time': end_time - start_time,\n",
            "                'memory_used_mb': max(0, end_memory - start_memory),\n",
            "                'peak_memory_mb': peak / (1024 ** 2),\n",
            "                'num_sentences': len(sentences),\n",
            "                'summary_sentences': summary_length,\n",
            "                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100),\n",
            "                'num_processes': self.num_processes,\n",
            "                'num_chunks': num_chunks\n",
            "            }\n",
            "            \n",
            "            return summary, metrics\n",
            "            \n",
            "        except Exception as e:\n",
            "            tracemalloc.stop()\n",
            "            return text, {\n",
            "                'execution_time': time.perf_counter() - start_time,\n",
            "                'memory_used_mb': 0,\n",
            "                'peak_memory_mb': 0,\n",
            "                'num_sentences': 0,\n",
            "                'summary_sentences': 0,\n",
            "                'compression_ratio': 0,\n",
            "                'num_processes': self.num_processes,\n",
            "                'num_chunks': 0\n",
            "            }\n",
            "\n",
            "print(\"ParallelTextRankSummarizer class defined (optimized)!\")"
        ]
    }
    
    return [
        textrank_sequential,
        textrank_seq_code,
        textrank_parallel_title,
        textrank_par_code
    ]

def main():
    print("Loading project.ipynb...")
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    print("Creating TextRank cells...")
    new_cells = create_textrank_cells()
    
    # Find where to insert (after TF-IDF Parallel cells)
    # Look for the cell with "ParallelTFIDFSummarizer class defined"
    insert_index = None
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code' and 'source' in cell:
            source = ''.join(cell['source'])
            if 'ParallelTFIDFSummarizer class defined' in source:
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
    
    print("\n[OK] TextRank summarizers added successfully!")
    print(f"\nAdded {len(new_cells)} new cells:")
    print("1. TextRank Sequential Summarizer (title)")
    print("2. TextRank Sequential Summarizer (code)")
    print("3. TextRank Parallel Summarizer (title)")
    print("4. TextRank Parallel Summarizer (code)")
    print("\nNext: Add cells to run TextRank and compare with TF-IDF")

if __name__ == "__main__":
    main()
