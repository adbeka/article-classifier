"""
Sentiment analysis module for analyzing article sentiment and emotional tone.
"""
from transformers import pipeline
from typing import Dict, List
from src.config import Config


class SentimentAnalyzer:
    """Analyzer for determining sentiment and emotional tone of articles."""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the sentiment analyzer with a pre-trained model.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)
        # For emotion detection, use a more advanced model
        try:
            self.emotion_pipeline = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None
            )
            self.has_emotion = True
        except Exception:
            # Fallback if emotion model is not available
            self.emotion_pipeline = None
            self.has_emotion = False
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyze the sentiment of the given text.
        
        Args:
            text: The article text to analyze
            
        Returns:
            Dictionary with sentiment label and confidence score
        """
        # Truncate text to avoid token limits
        words = text.split()[:512]
        text_truncated = ' '.join(words)
        
        if not text_truncated:
            return {
                'label': 'NEUTRAL',
                'score': 0.0
            }
        
        result = self.sentiment_pipeline(text_truncated)[0]
        
        return {
            'label': result['label'],
            'score': result['score']
        }
    
    def analyze_emotions(self, text: str) -> List[Dict[str, any]]:
        """
        Analyze emotions present in the text.
        
        Args:
            text: The article text to analyze
            
        Returns:
            List of emotions with their scores (sorted by score)
        """
        if not self.has_emotion:
            return []
        
        # Truncate text to avoid token limits
        words = text.split()[:512]
        text_truncated = ' '.join(words)
        
        if not text_truncated:
            return []
        
        try:
            emotions = self.emotion_pipeline(text_truncated)[0]
            # Sort by score (descending)
            emotions_sorted = sorted(emotions, key=lambda x: x['score'], reverse=True)
            return emotions_sorted[:5]  # Return top 5 emotions
        except Exception:
            return []
    
    def analyze_article(self, article: Dict[str, str]) -> Dict[str, str]:
        """
        Analyze sentiment and emotions of an article.
        
        Args:
            article: Article dictionary with 'text' and 'title' keys
            
        Returns:
            Article dictionary with added 'sentiment_analysis' key
        """
        # Combine title and text for better analysis
        text_to_analyze = f"{article.get('title', '')} {article.get('text', '')}"
        
        sentiment = self.analyze_sentiment(text_to_analyze)
        emotions = self.analyze_emotions(text_to_analyze)
        
        article['sentiment_analysis'] = {
            'sentiment': sentiment,
            'emotions': emotions
        }
        
        return article
    
    def get_sentiment_emoji(self, sentiment_label: str) -> str:
        """
        Get an emoji representation of the sentiment.
        
        Args:
            sentiment_label: Sentiment label (POSITIVE, NEGATIVE, NEUTRAL)
            
        Returns:
            Emoji string
        """
        emoji_map = {
            'POSITIVE': '😊',
            'NEGATIVE': '😞',
            'NEUTRAL': '😐'
        }
        return emoji_map.get(sentiment_label.upper(), '🤔')
