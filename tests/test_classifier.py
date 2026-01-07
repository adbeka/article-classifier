"""
Tests for the article classifier module.
"""
import unittest
from unittest.mock import Mock, patch
from src.classifier import ArticleClassifier


class TestArticleClassifier(unittest.TestCase):
    """Test cases for ArticleClassifier class."""
    
    @patch('src.classifier.pipeline')
    def setUp(self, mock_pipeline):
        """Set up test fixtures."""
        self.mock_classifier = Mock()
        mock_pipeline.return_value = self.mock_classifier
        self.classifier = ArticleClassifier()
    
    def test_classifier_initialization(self):
        """Test that classifier initializes correctly."""
        self.assertIsNotNone(self.classifier)
        self.assertIsNotNone(self.classifier.default_labels)
        self.assertGreater(len(self.classifier.default_labels), 0)
    
    def test_classify_with_default_labels(self):
        """Test classification with default labels."""
        self.mock_classifier.return_value = {
            'labels': ['technology', 'business', 'science'],
            'scores': [0.9, 0.7, 0.5]
        }
        
        result = self.classifier.classify("This is an article about AI technology.")
        
        self.assertIn('top_label', result)
        self.assertIn('top_score', result)
        self.assertEqual(result['top_label'], 'technology')
        self.assertEqual(result['top_score'], 0.9)
    
    def test_classify_article(self):
        """Test classifying an article dictionary."""
        self.mock_classifier.return_value = {
            'labels': ['sports', 'entertainment'],
            'scores': [0.85, 0.6]
        }
        
        article = {
            'title': 'Sports News',
            'text': 'An article about football.'
        }
        
        result = self.classifier.classify_article(article)
        
        self.assertIn('classification', result)
        self.assertEqual(result['classification']['top_label'], 'sports')


if __name__ == '__main__':
    unittest.main()
