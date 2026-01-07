"""
Article classifier module using NLP for topic classification.
"""
from transformers import pipeline
from typing import List, Dict


class ArticleClassifier:
    """Classifier for categorizing articles by topic using zero-shot classification."""
    
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """
        Initialize the classifier with a pre-trained model.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.classifier = pipeline("zero-shot-classification", model=model_name)
        self.default_labels = [
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
    
    def classify(self, text: str, labels: List[str] = None) -> Dict[str, any]:
        """
        Classify article text into topics.
        
        Args:
            text: The article text to classify
            labels: Optional list of custom labels. Uses default if not provided.
            
        Returns:
            Dictionary with 'labels' and 'scores' for each classification
        """
        if labels is None:
            labels = self.default_labels
        
        # Truncate text to avoid token limits
        from src.config import Config
        text_truncated = ' '.join(text.split()[:Config.MAX_CLASSIFICATION_WORDS])
        
        result = self.classifier(text_truncated, labels, multi_label=True)
        
        return {
            'top_label': result['labels'][0],
            'top_score': result['scores'][0],
            'all_labels': result['labels'],
            'all_scores': result['scores']
        }
    
    def classify_article(self, article: Dict[str, str], labels: List[str] = None) -> Dict[str, any]:
        """
        Classify an article dictionary.
        
        Args:
            article: Article dictionary with 'text' and 'title' keys
            labels: Optional list of custom labels
            
        Returns:
            Article dictionary with added 'classification' key
        """
        # Use title + text for better classification
        text_to_classify = f"{article.get('title', '')} {article.get('text', '')}"
        classification = self.classify(text_to_classify, labels)
        
        article['classification'] = classification
        return article
