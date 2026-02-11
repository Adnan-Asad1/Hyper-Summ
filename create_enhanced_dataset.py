"""
Create improved dataset with longer articles for better TF-IDF demonstration
This will combine multiple short descriptions into longer articles
"""

import json
import random

def create_longer_articles(input_file='News_Category_Dataset_v3.json', output_file='enhanced_articles.json', num_articles=10):
    """
    Create longer synthetic articles by combining multiple short descriptions
    """
    
    print(f"Loading {input_file}...")
    articles_data = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                article = json.loads(line.strip())
                articles_data.append(article)
            except:
                continue
    
    print(f"Loaded {len(articles_data)} articles")
    
    # Group by category
    by_category = {}
    for article in articles_data:
        category = article.get('category', 'Unknown')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(article)
    
    print(f"Found {len(by_category)} categories")
    
    # Create longer articles
    enhanced_articles = []
    
    for category, articles in list(by_category.items())[:num_articles]:
        # Take 5-8 articles from same category and combine them
        num_to_combine = min(random.randint(5, 8), len(articles))
        selected = random.sample(articles, num_to_combine)
        
        # Combine descriptions
        combined_text = ' '.join([
            art.get('short_description', '') 
            for art in selected 
            if art.get('short_description')
        ])
        
        # Create enhanced article
        enhanced = {
            'id': len(enhanced_articles),
            'category': category,
            'article': combined_text,
            'num_words': len(combined_text.split()),
            'num_sentences': combined_text.count('.') + combined_text.count('!') + combined_text.count('?'),
            'source_articles': num_to_combine
        }
        
        enhanced_articles.append(enhanced)
        
        print(f"Created article {len(enhanced_articles)}: {category} - {enhanced['num_words']} words, {enhanced['num_sentences']} sentences")
    
    # Save enhanced articles
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_articles, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Created {len(enhanced_articles)} enhanced articles")
    print(f"Average length: {sum(a['num_words'] for a in enhanced_articles) / len(enhanced_articles):.0f} words")
    
    return enhanced_articles

if __name__ == "__main__":
    create_longer_articles(num_articles=10)
