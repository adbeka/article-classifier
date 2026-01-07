"""
Main application module integrating scraper, classifier, and summarizer.
"""
from src.scraper import ArticleScraper
from src.classifier import ArticleClassifier
from src.summarizer import ArticleSummarizer
from src.config import Config
from typing import Dict, List


class ArticleProcessor:
    """Main processor that integrates all components."""
    
    def __init__(self):
        """Initialize all components."""
        self.scraper = ArticleScraper()
        self.classifier = ArticleClassifier(model_name=Config.CLASSIFIER_MODEL)
        self.summarizer = ArticleSummarizer(model_name=Config.SUMMARIZER_MODEL)
    
    def process_url(self, url: str) -> Dict:
        """
        Process a single URL: scrape, classify, and summarize.
        
        Args:
            url: The URL of the article to process
            
        Returns:
            Processed article dictionary with all information
        """
        # Scrape the article
        article = self.scraper.scrape_url(url)
        if not article:
            return {'error': 'Failed to scrape article'}
        
        # Classify the article
        article = self.classifier.classify_article(article)
        
        # Summarize the article
        article = self.summarizer.summarize_article(
            article,
            max_length=Config.SUMMARY_MAX_LENGTH,
            min_length=Config.SUMMARY_MIN_LENGTH
        )
        
        return article
    
    def process_urls(self, urls: List[str]) -> List[Dict]:
        """
        Process multiple URLs.
        
        Args:
            urls: List of URLs to process
            
        Returns:
            List of processed article dictionaries
        """
        results = []
        for url in urls:
            result = self.process_url(url)
            results.append(result)
        return results


def main():
    """Example usage of the article processor."""
    processor = ArticleProcessor()
    
    # Example URLs (these should be replaced with actual news URLs)
    example_urls = [
        "https://www.bbc.com/news/technology-12345678",
        # Add more URLs as needed
    ]
    
    print("Article Classifier & Summarizer")
    print("=" * 50)
    
    for url in example_urls:
        print(f"\nProcessing: {url}")
        result = processor.process_url(url)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
            continue
        
        print(f"\nTitle: {result.get('title', 'N/A')}")
        print(f"Category: {result['classification']['top_label']} (Score: {result['classification']['top_score']:.2f})")
        print(f"\nSummary:\n{result.get('summary', 'N/A')}")
        print("-" * 50)


if __name__ == "__main__":
    main()
