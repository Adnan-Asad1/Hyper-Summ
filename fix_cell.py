import json

# Read the notebook
with open('project.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the dataset loading cell
for cell in notebook['cells']:
    if cell.get('id') == '05ed9913':
        # Replace with properly formatted source (each line is a separate string)
        cell['source'] = [
            "import os\n",
            "import json\n",
            "import requests\n",
            "from pathlib import Path\n",
            "from io import StringIO\n",
            "\n",
            "print(\"Loading CNN Daily Mail / News Category dataset...\")\n",
            "print(\"Dataset: News_Category_Dataset_v3.json\")\n",
            "\n",
            "# Load the actual News Category Dataset\n",
            "dataset_path = \"News_Category_Dataset_v3.json\"\n",
            "\n",
            "if os.path.exists(dataset_path):\n",
            "    print(f\"✓ Found dataset at: {os.path.abspath(dataset_path)}\")\n",
            "    \n",
            "    # Load JSON dataset - MODIFIED TO CREATE LONGER ARTICLES\n",
            "    all_articles = []\n",
            "    try:\n",
            "        with open(dataset_path, 'r', encoding='utf-8') as f:\n",
            "            for line in f:\n",
            "                try:\n",
            "                    article = json.loads(line.strip())\n",
            "                    all_articles.append(article)\n",
            "                except json.JSONDecodeError:\n",
            "                    continue\n",
            "        \n",
            "        # Create longer articles by combining 3-5 related articles from same category\n",
            "        articles_data = []\n",
            "        categories = {}\n",
            "        \n",
            "        # Group by category\n",
            "        for article in all_articles:\n",
            "            cat = article.get('category', 'Unknown')\n",
            "            if cat not in categories:\n",
            "                categories[cat] = []\n",
            "            categories[cat].append(article)\n",
            "        \n",
            "        # Combine articles from same category\n",
            "        for category, cat_articles in categories.items():\n",
            "            i = 0\n",
            "            while i < len(cat_articles) and len(articles_data) < 100:\n",
            "                # Take 3-5 articles and combine them\n",
            "                num_to_combine = min(4, len(cat_articles) - i)  # Combine 4 articles\n",
            "                combined_articles = cat_articles[i:i+num_to_combine]\n",
            "                \n",
            "                # Create combined article text\n",
            "                combined_text = ' '.join([\n",
            "                    art.get('headline', '') + '. ' + art.get('short_description', '')\n",
            "                    for art in combined_articles\n",
            "                ])\n",
            "                \n",
            "                # Use first article's short_description as reference summary\n",
            "                reference_summary = combined_articles[0].get('short_description', '')\n",
            "                \n",
            "                articles_data.append({\n",
            "                    'id': len(articles_data),\n",
            "                    'article': combined_text,\n",
            "                    'summary': reference_summary,\n",
            "                    'category': category,\n",
            "                    'date': combined_articles[0].get('date', '2024-01-01')\n",
            "                })\n",
            "                \n",
            "                i += num_to_combine\n",
            "                \n",
            "                if len(articles_data) >= 100:\n",
            "                    break\n",
            "        \n",
            "        df = pd.DataFrame(articles_data[:100])\n",
            "        \n",
            "        print(f\"✓ Successfully loaded {len(df)} articles from dataset\")\n",
            "        print(f\"✓ Dataset shape: {df.shape}\")\n",
            "        \n",
            "    except Exception as e:\n",
            "        print(f\"✗ Error loading dataset: {e}\")\n",
            "        raise Exception(\"Could not load dataset from file\")\n",
            "else:\n",
            "    print(f\"✗ Dataset file not found at: {os.path.abspath(dataset_path)}\")\n",
            "    raise Exception(\"Dataset file not found\")\n",
            "\n",
            "# Display dataset info\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"DATASET SUMMARY\")\n",
            "print(f\"{'='*80}\")\n",
            "print(f\"Total articles: {len(df)}\")\n",
            "print(f\"Columns: {df.columns.tolist()}\")\n",
            "print(f\"\\nSample article length: {len(df['article'].iloc[0].split())} words\")\n",
            "if 'summary' in df.columns:\n",
            "    print(f\"Sample summary length: {len(df['summary'].iloc[0].split())} words\")\n",
            "print(f\"\\nFirst article preview:\")\n",
            "print(df['article'].iloc[0][:300] + \"...\")\n",
            "print(f\"\\nCategories in dataset: {df['category'].unique()[:10] if 'category' in df.columns else 'N/A'}\")"
        ]
        print("Fixed cell 05ed9913")
        break

# Save the corrected notebook
with open('project.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Notebook fixed successfully!")
print("Now you can run the cells in Jupyter - the \\n characters are removed.")
