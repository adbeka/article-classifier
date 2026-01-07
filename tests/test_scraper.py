"""
Tests for the article scraper module.
"""
import unittest
from unittest.mock import Mock, patch
from src.scraper import ArticleScraper


class TestArticleScraper(unittest.TestCase):
    """Test cases for ArticleScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = ArticleScraper()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        self.assertIsNotNone(self.scraper)
        self.assertIsNotNone(self.scraper.headers)
        self.assertIn('User-Agent', self.scraper.headers)
    
    @patch('src.scraper.Article')
    def test_scrape_url_success(self, mock_article):
        """Test successful article scraping."""
        # Mock the Article class
        mock_instance = Mock()
        mock_instance.title = "Test Article"
        mock_instance.text = "This is test content."
        mock_instance.authors = ["Test Author"]
        mock_instance.publish_date = None
        mock_instance.top_image = "http://example.com/image.jpg"
        mock_article.return_value = mock_instance
        
        result = self.scraper.scrape_url("http://example.com/article")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Test Article")
        self.assertEqual(result['text'], "This is test content.")
        self.assertEqual(result['url'], "http://example.com/article")
    
    @patch('src.scraper.Article')
    def test_scrape_url_failure(self, mock_article):
        """Test handling of scraping failures."""
        mock_article.side_effect = Exception("Network error")
        
        result = self.scraper.scrape_url("http://example.com/article")
        
        self.assertIsNone(result)
    
    def test_scrape_multiple_empty_list(self):
        """Test scraping with empty URL list."""
        result = self.scraper.scrape_multiple([])
        
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
