"""
Simple script to fix the project.ipynb notebook
Directly modifies the JSON structure
"""

import json

def main():
    print("Loading project.ipynb...")
    with open('project.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Find and fix the calculate_dynamic_summary_length function
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and 'source' in cell:
            source = ''.join(cell['source'])
            
            # Fix calculate_dynamic_summary_length
            if 'def calculate_dynamic_summary_length' in source:
                print("Found calculate_dynamic_summary_length function, fixing...")
                
                new_source = [
                    "def preprocess_text(text: str) -> Tuple[List[str], str]:\n",
                    "    \"\"\"\n",
                    "    Preprocess text: tokenize into sentences and clean\n",
                    "    Returns: (sentences, cleaned_text)\n",
                    "    \"\"\"\n",
                    "    # Remove extra whitespace and newlines first\n",
                    "    text = ' '.join(text.split())\n",
                    "    \n",
                    "    # Sentence tokenization\n",
                    "    sentences = sent_tokenize(text)\n",
                    "    \n",
                    "    # Remove empty sentences\n",
                    "    sentences = [s.strip() for s in sentences if s.strip()]\n",
                    "    \n",
                    "    # Clean text\n",
                    "    cleaned_text = text.lower()\n",
                    "    cleaned_text = re.sub(r'[^\\w\\s]', ' ', cleaned_text)\n",
                    "    cleaned_text = re.sub(r'\\s+', ' ', cleaned_text).strip()\n",
                    "    \n",
                    "    return sentences, cleaned_text\n",
                    "\n",
                    "def chunk_by_paragraphs(text: str, min_chunk_size: int = 100) -> List[str]:\n",
                    "    \"\"\"\n",
                    "    Split text into chunks by paragraphs\n",
                    "    \"\"\"\n",
                    "    paragraphs = [p.strip() for p in text.split('\\n\\n') if p.strip()]\n",
                    "    \n",
                    "    if not paragraphs:\n",
                    "        # If no paragraph breaks, split by sentences\n",
                    "        sentences = sent_tokenize(text)\n",
                    "        chunks = []\n",
                    "        current_chunk = []\n",
                    "        \n",
                    "        for sentence in sentences:\n",
                    "            current_chunk.append(sentence)\n",
                    "            if len(' '.join(current_chunk).split()) >= min_chunk_size:\n",
                    "                chunks.append(' '.join(current_chunk))\n",
                    "                current_chunk = []\n",
                    "        \n",
                    "        if current_chunk:\n",
                    "            chunks.append(' '.join(current_chunk))\n",
                    "        return chunks\n",
                    "    \n",
                    "    return paragraphs\n",
                    "\n",
                    "def calculate_dynamic_summary_length(num_sentences: int) -> int:\n",
                    "    \"\"\"\n",
                    "    Calculate dynamic summary length based on document size\n",
                    "    Rule: 30-35% of original sentences, minimum 1, maximum num_sentences-1\n",
                    "    Ensures summary is ALWAYS shorter than original for proper compression\n",
                    "    \"\"\"\n",
                    "    if num_sentences <= 2:\n",
                    "        return 1\n",
                    "    # Summary should be 30-35% of original, but always less than original\n",
                    "    summary_length = max(1, min(num_sentences - 1, int(num_sentences * 0.35)))\n",
                    "    return summary_length\n",
                    "\n",
                    "def get_performance_metrics() -> Dict:\n",
                    "    \"\"\"\n",
                    "    Get current system performance metrics\n",
                    "    \"\"\"\n",
                    "    process = psutil.Process()\n",
                    "    return {\n",
                    "        'cpu_percent': process.cpu_percent(interval=0.1),\n",
                    "        'memory_rss_mb': process.memory_info().rss / (1024 ** 2),\n",
                    "        'memory_vms_mb': process.memory_info().vms / (1024 ** 2)\n",
                    "    }\n",
                    "\n",
                    "print(\"Utility functions defined successfully!\")"
                ]
                
                cell['source'] = new_source
                print("[OK] Fixed calculate_dynamic_summary_length")
    
    print("Saving fixed notebook...")
    with open('project.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("\n[OK] Notebook fixed successfully!")
    print("\nChanges made:")
    print("1. Updated calculate_dynamic_summary_length to ensure summary < original")
    print("2. Summary length now: max(1, min(num_sentences-1, 35% of original))")
    print("\nNext: Open project.ipynb and run all cells")

if __name__ == "__main__":
    main()
