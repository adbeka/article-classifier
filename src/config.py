"""
Configuration settings for the article classifier application.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Flask API Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Model Configuration
    CLASSIFIER_MODEL = os.getenv('CLASSIFIER_MODEL', 'facebook/bart-large-mnli')
    SUMMARIZER_MODEL = os.getenv('SUMMARIZER_MODEL', 'facebook/bart-large-cnn')
    
    # Summary Configuration
    SUMMARY_MAX_LENGTH = int(os.getenv('SUMMARY_MAX_LENGTH', 130))
    SUMMARY_MIN_LENGTH = int(os.getenv('SUMMARY_MIN_LENGTH', 30))
    
    # Classifier Configuration
    MAX_CLASSIFICATION_WORDS = int(os.getenv('MAX_CLASSIFICATION_WORDS', 500))
    
    # API Configuration
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 10))
    
    # Summarizer Configuration
    MAX_SUMMARIZER_INPUT_LENGTH = int(os.getenv('MAX_SUMMARIZER_INPUT_LENGTH', 1024))
    
    # Classification Labels
    CLASSIFICATION_LABELS = [
        "politics",
        "technology",
        "business",
        "entertainment",
        "sports",
        "science",
        "health",
        "environment",
        "education",
        "world news"
    ]
