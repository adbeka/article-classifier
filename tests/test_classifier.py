"""
Tests for the article classifier module.
"""
import unittest
from unittest.mock import Mock, patch
from src.classifier import ArticleClassifier


class TestArticleClassifier(unittest.TestCase):
    """Test cases for ArticleClassifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_classifier = Mock()
        
    @patch('src.classifier.pipeline')
    def test_classifier_initialization(self, mock_pipeline):
        """Test that classifier initializes correctly."""
        mock_pipeline.return_value = self.mock_classifier
        classifier = ArticleClassifier()
        self.assertIsNotNone(classifier)
        self.assertIsNotNone(classifier.default_labels)
        self.assertGreater(len(classifier.default_labels), 0)
    
    @patch('src.classifier.pipeline')
    def test_classify_with_default_labels(self, mock_pipeline):
        """Test classification with default labels."""
        mock_pipeline.return_value = self.mock_classifier
        self.mock_classifier.return_value = {
            'labels': ['technology', 'business', 'science'],
            'scores': [0.9, 0.7, 0.5]
        }
        
        classifier = ArticleClassifier()
        result = classifier.classify("This is an article about AI technology.")
        
        self.assertIn('top_label', result)
        self.assertIn('top_score', result)
        self.assertEqual(result['top_label'], 'technology')
        self.assertEqual(result['top_score'], 0.9)
    
    @patch('src.classifier.pipeline')
    def test_classify_article(self, mock_pipeline):
        """Test classifying an article dictionary."""
        mock_pipeline.return_value = self.mock_classifier
        self.mock_classifier.return_value = {
            'labels': ['sports', 'entertainment'],
            'scores': [0.85, 0.6]
        }
        
        classifier = ArticleClassifier()
        article = {
            'title': 'Sports News',
            'text': 'An article about football.'
        }
        
        result = classifier.classify_article(article)
        
        self.assertIn('classification', result)
        self.assertEqual(result['classification']['top_label'], 'sports')


if __name__ == '__main__':
    unittest.main()
