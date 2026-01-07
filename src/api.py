"""
Flask API backend for Chrome extension.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.main import ArticleProcessor
from src.config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# Initialize processor
processor = ArticleProcessor()


@app.route('/')
def index():
    """API root endpoint."""
    return jsonify({
        'message': 'Article Classifier & Summarizer API',
        'version': '1.0',
        'endpoints': {
            '/api/process': 'POST - Process a single URL',
            '/api/health': 'GET - Health check'
        }
    })


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


@app.route('/api/process', methods=['POST'])
def process_article():
    """
    Process a single article URL.
    
    Expected JSON body:
    {
        "url": "https://example.com/article"
    }
    
    Returns:
    {
        "title": "...",
        "text": "...",
        "summary": "...",
        "classification": {
            "top_label": "...",
            "top_score": 0.95,
            ...
        },
        "url": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Process the article
        result = processor.process_url(url)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch', methods=['POST'])
def process_batch():
    """
    Process multiple article URLs.
    
    Expected JSON body:
    {
        "urls": ["url1", "url2", ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({'error': 'URLs array is required'}), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list):
            return jsonify({'error': 'URLs must be an array'}), 400
        
        if len(urls) > 10:
            return jsonify({'error': 'Maximum 10 URLs allowed per batch'}), 400
        
        # Process the articles
        results = processor.process_urls(urls)
        
        return jsonify({'results': results})
        
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        return jsonify({'error': str(e)}), 500


def main():
    """Start the Flask API server."""
    print(f"Starting API server on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )


if __name__ == '__main__':
    main()
