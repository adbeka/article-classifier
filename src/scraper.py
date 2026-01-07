"""
Article scraper module for extracting content from news URLs.
"""
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from typing import Dict, Optional


class ArticleScraper:
    """Scraper for extracting article content from URLs."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def scrape_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape an article from a given URL.
        
        Args:
            url: The URL of the article to scrape
            
        Returns:
            Dictionary containing title, text, authors, publish_date, and url
            Returns None if scraping fails
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else None,
                'url': url,
                'top_image': article.top_image
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def scrape_multiple(self, urls: list) -> list:
        """
        Scrape multiple articles from a list of URLs.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of article dictionaries
        """
        articles = []
        for url in urls:
            article = self.scrape_url(url)
            if article:
                articles.append(article)
        return articles
