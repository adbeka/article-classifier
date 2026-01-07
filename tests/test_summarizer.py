"""
Tests for the article summarizer module.
"""
import unittest
from unittest.mock import Mock, patch
from src.summarizer import ArticleSummarizer


class TestArticleSummarizer(unittest.TestCase):
    """Test cases for ArticleSummarizer class."""
    
    @patch('src.summarizer.pipeline')
    def setUp(self, mock_pipeline):
        """Set up test fixtures."""
        self.mock_summarizer = Mock()
        mock_pipeline.return_value = self.mock_summarizer
        self.summarizer = ArticleSummarizer()
    
    def test_summarizer_initialization(self):
        """Test that summarizer initializes correctly."""
        self.assertIsNotNone(self.summarizer)
        self.assertIsNotNone(self.summarizer.summarizer)
    
    def test_summarize_short_text(self):
        """Test summarizing short text."""
        self.mock_summarizer.return_value = [
            {'summary_text': 'This is a summary.'}
        ]
        
        text = "This is a test article that needs to be summarized."
        result = self.summarizer.summarize(text)
        
        self.assertEqual(result, 'This is a summary.')
    
    def test_summarize_article(self):
        """Test summarizing an article dictionary."""
        self.mock_summarizer.return_value = [
            {'summary_text': 'Article summary.'}
        ]
        
        article = {
            'title': 'Test Article',
            'text': 'This is the full text of the article.'
        }
        
        result = self.summarizer.summarize_article(article)
        
        self.assertIn('summary', result)
        self.assertEqual(result['summary'], 'Article summary.')
    
    def test_summarize_article_empty_text(self):
        """Test summarizing article with empty text."""
        article = {'title': 'Test', 'text': ''}
        
        result = self.summarizer.summarize_article(article)
        
        self.assertEqual(result['summary'], '')


if __name__ == '__main__':
    unittest.main()
