"""
Flask Web Application for Text Summarization
Provides REST API and web interface for text summarization
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import nltk
from summarizers import (
    SequentialTextRankSummarizer,
    ParallelTextRankSummarizer,
    SequentialTFIDFSummarizer,
    ParallelTFIDFSummarizer
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Download NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Initialize summarizers
summarizers = {
    'textrank_seq': SequentialTextRankSummarizer(),
    'textrank_par': ParallelTextRankSummarizer(),
    'tfidf_seq': SequentialTFIDFSummarizer(),
    'tfidf_par': ParallelTFIDFSummarizer()
}


@app.route('/')
def index():
    """Serve the main UI page"""
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    API endpoint to generate summary
    
    Request JSON:
    {
        "text": "Article text here...",
        "algorithm": "textrank_seq|textrank_par|tfidf_seq|tfidf_par"
    }
    
    Response JSON:
    {
        "success": true,
        "original_text": "...",
        "summary": "...",
        "metrics": {...}
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        text = data.get('text', '').strip()
        algorithm = data.get('algorithm', 'textrank_seq')
        
        # Validate input
        if not text:
            return jsonify({
                'success': False,
                'error': 'Please provide text to summarize'
            }), 400
        
        if len(text.split()) < 10:
            return jsonify({
                'success': False,
                'error': 'Text is too short. Please provide at least 10 words.'
            }), 400
        
        if algorithm not in summarizers:
            return jsonify({
                'success': False,
                'error': f'Invalid algorithm: {algorithm}'
            }), 400
        
        # Generate summary
        summarizer = summarizers[algorithm]
        summary, metrics = summarizer.summarize(text)
        
        # Prepare response
        response = {
            'success': True,
            'original_text': text,
            'original_word_count': len(text.split()),
            'summary': summary,
            'summary_word_count': len(summary.split()),
            'metrics': {
                'execution_time': round(metrics['execution_time'], 4),
                'compression_ratio': round(metrics['compression_ratio'], 2),
                'memory_used_mb': round(metrics['memory_used_mb'], 2),
                'peak_memory_mb': round(metrics['peak_memory_mb'], 2),
                'num_sentences': metrics['num_sentences'],
                'summary_sentences': metrics['summary_sentences']
            },
            'algorithm_name': {
                'textrank_seq': 'TextRank Sequential',
                'textrank_par': 'TextRank Parallel',
                'tfidf_seq': 'TF-IDF Sequential',
                'tfidf_par': 'TF-IDF Parallel'
            }[algorithm]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'algorithms': list(summarizers.keys())
    })


if __name__ == '__main__':
    print("=" * 80)
    print("TEXT SUMMARIZATION WEB UI")
    print("=" * 80)
    print("Server starting...")
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)
