"""
Main application module integrating scraper, classifier, and summarizer.
"""
from src.scraper import ArticleScraper
from src.classifier import ArticleClassifier
from src.summarizer import ArticleSummarizer
from src.sentiment_analyzer import SentimentAnalyzer
from src.keyword_extractor import KeywordExtractor
from src.metadata_analyzer import MetadataAnalyzer
from src.similarity_analyzer import SimilarityAnalyzer
from src.database import ArticleDatabase
from src.exporter import ArticleExporter
from src.config import Config
from typing import Dict, List, Optional


class ArticleProcessor:
    """Main processor that integrates all components."""
    
    def __init__(self, use_cache: bool = True, use_advanced_features: bool = True):
        """
        Initialize all components.
        
        Args:
            use_cache: Whether to use database caching
            use_advanced_features: Whether to enable sentiment, keyword, and metadata analysis
        """
        self.scraper = ArticleScraper()
        self.classifier = ArticleClassifier(model_name=Config.CLASSIFIER_MODEL)
        self.summarizer = ArticleSummarizer(model_name=Config.SUMMARIZER_MODEL)
        
        # Advanced features
        self.use_advanced_features = use_advanced_features
        if use_advanced_features:
            self.sentiment_analyzer = SentimentAnalyzer()
            self.keyword_extractor = KeywordExtractor()
            self.metadata_analyzer = MetadataAnalyzer()
            self.similarity_analyzer = SimilarityAnalyzer()
        
        # Database and export
        self.use_cache = use_cache
        if use_cache:
            self.db = ArticleDatabase()
        self.exporter = ArticleExporter()
    
    
    def process_url(self, url: str, force_refresh: bool = False) -> Dict:
        """
        Process a single URL: scrape, classify, and summarize.
        
        Args:
            url: The URL of the article to process
            force_refresh: Force re-processing even if cached
            
        Returns:
            Processed article dictionary with all information
        """
        # Check cache first
        if self.use_cache and not force_refresh:
            cached_article = self.db.get_article(url, max_age_hours=24)
            if cached_article:
                return cached_article
        
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
        
        # Apply advanced features
        if self.use_advanced_features:
            article = self.sentiment_analyzer.analyze_article(article)
            article = self.keyword_extractor.analyze_article(article)
            article = self.metadata_analyzer.analyze_article(article)
            
            # Generate embedding for similarity analysis
            embedding = self.similarity_analyzer.generate_article_embedding(article)
            article['embedding'] = embedding
        
        # Cache the result
        if self.use_cache:
            self.db.save_article(article)
        
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
    
    def export_article(self, article: Dict, format: str = "json", filename: str = None) -> str:
        """
        Export article to a file.
        
        Args:
            article: Article dictionary
            format: Export format ('json', 'markdown', 'html', 'csv')
            filename: Optional custom filename
            
        Returns:
            Path to the exported file
        """
        if format == "json":
            return self.exporter.export_to_json(article, filename)
        elif format == "markdown":
            return self.exporter.export_to_markdown(article, filename)
        elif format == "html":
            return self.exporter.export_to_html(article, filename)
        elif format == "csv":
            return self.exporter.export_to_csv([article], filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_cached_articles(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Retrieve cached articles from database.
        
        Args:
            category: Filter by category
            limit: Maximum number of articles to return
            
        Returns:
            List of cached articles
        """
        if not self.use_cache:
            return []
        return self.db.search_articles(category=category, limit=limit)
    
    def get_statistics(self) -> Dict:
        """
        Get processing statistics from database.
        
        Returns:
            Dictionary with statistics
        """
        if not self.use_cache:
            return {}
        return self.db.get_statistics()
    
    def cleanup_old_cache(self, days: int = 30) -> int:
        """
        Clean up old cached articles.
        
        Args:
            days: Delete articles older than this many days
            
        Returns:
            Number of articles deleted
        """
        if not self.use_cache:
            return 0
        return self.db.clear_old_articles(days)
    
    def find_similar_articles(
        self,
        article: Dict,
        top_k: int = 5,
        min_similarity: float = 0.5
    ) -> List[Dict]:
        """
        Find similar articles to the given article.
        
        Args:
            article: Article dictionary (must have embedding or will generate one)
            top_k: Number of similar articles to return
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            List of similar articles with similarity scores
        """
        if not self.use_advanced_features:
            return []
        
        # Get or generate embedding for the article
        if 'embedding' not in article or article['embedding'] is None:
            article['embedding'] = self.similarity_analyzer.generate_article_embedding(article)
        
        # Get all cached articles with embeddings
        if self.use_cache:
            cached_articles = self.db.get_all_articles_with_embeddings()
        else:
            return []
        
        # Find similar articles
        similar = self.similarity_analyzer.find_similar_articles(
            article,
            cached_articles,
            top_k=top_k,
            min_similarity=min_similarity
        )
        
        return similar
    
    def find_similar_by_url(
        self,
        url: str,
        top_k: int = 5,
        min_similarity: float = 0.5
    ) -> List[Dict]:
        """
        Find similar articles by URL.
        
        Args:
            url: URL of the article
            top_k: Number of similar articles to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar articles with similarity scores
        """
        # Process or get cached article
        article = self.process_url(url)
        if 'error' in article:
            return []
        
        return self.find_similar_articles(article, top_k, min_similarity)
    
    def check_duplicate(
        self,
        article: Dict,
        threshold: float = 0.9
    ) -> Dict:
        """
        Check if an article is a duplicate of existing articles.
        
        Args:
            article: Article dictionary
            threshold: Similarity threshold for duplicate detection
            
        Returns:
            Dictionary with duplicate information
        """
        if not self.use_advanced_features:
            return {'is_duplicate': False, 'duplicates': []}
        
        similar = self.find_similar_articles(article, top_k=10, min_similarity=threshold)
        
        return {
            'is_duplicate': len(similar) > 0,
            'duplicate_count': len(similar),
            'duplicates': [
                {
                    'title': s['article'].get('title'),
                    'url': s['article'].get('url'),
                    'similarity': s['similarity_score']
                }
                for s in similar
            ]
        }
    
    def find_all_duplicates(self, threshold: float = 0.9) -> List[Dict]:
        """
        Find all duplicate articles in the database.
        
        Args:
            threshold: Similarity threshold for duplicate detection
            
        Returns:
            List of duplicate pairs with similarity scores
        """
        if not self.use_cache or not self.use_advanced_features:
            return []
        
        duplicates = self.db.find_duplicates(threshold)
        
        return [
            {
                'article1': {
                    'title': dup[0].get('title'),
                    'url': dup[0].get('url')
                },
                'article2': {
                    'title': dup[1].get('title'),
                    'url': dup[1].get('url')
                },
                'similarity': dup[2]
            }
            for dup in duplicates
        ]
    
    def get_article_similarity_report(self, article: Dict) -> Dict:
        """
        Get comprehensive similarity report for an article.
        
        Args:
            article: Article dictionary
            
        Returns:
            Comprehensive similarity analysis
        """
        if not self.use_advanced_features or not self.use_cache:
            return {}
        
        cached_articles = self.db.get_all_articles_with_embeddings()
        return self.similarity_analyzer.analyze_article_similarity(article, cached_articles)


def main():
    """Example usage of the article processor."""
    processor = ArticleProcessor()
    
    # Example URLs (these should be replaced with actual news URLs)
    example_urls = [
        "https://www.bbc.com/news/technology-12345678",
        # Add more URLs as needed
    ]
    
    print("Article Classifier & Summarizer (Enhanced Edition)")
    print("=" * 70)
    
    for url in example_urls:
        print(f"\nProcessing: {url}")
        result = processor.process_url(url)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
            continue
        
        print(f"\n📰 Title: {result.get('title', 'N/A')}")
        print(f"🏷️  Category: {result['classification']['top_label'].upper()} ({result['classification']['top_score']*100:.1f}%)")
        
        # Sentiment
        if 'sentiment_analysis' in result:
            sentiment = result['sentiment_analysis']['sentiment']
            emoji = processor.sentiment_analyzer.get_sentiment_emoji(sentiment['label'])
            print(f"{emoji} Sentiment: {sentiment['label']} ({sentiment['score']*100:.1f}%)")
        
        # Reading time and quality
        if 'metadata_analysis' in result:
            metadata = result['metadata_analysis']
            reading_time = metadata['reading_time']
            quality = metadata['quality_score']
            print(f"⏱️  Reading Time: {reading_time['formatted']}")
            print(f"⭐ Quality Score: {quality['score']}/100 ({quality['grade']})")
        
        # Keywords
        if 'keyword_analysis' in result:
            keywords = result['keyword_analysis']['keywords'][:5]
            keyword_list = ', '.join([kw['word'] for kw in keywords])
            print(f"🔑 Top Keywords: {keyword_list}")
        
        print(f"\n📝 Summary:\n{result.get('summary', 'N/A')}")
        print("-" * 70)
    
    # Show statistics
    stats = processor.get_statistics()
    if stats:
        print(f"\n📊 Database Statistics:")
        print(f"Total Articles Cached: {stats['total_articles']}")
        if stats['category_distribution']:
            print(f"Category Distribution: {stats['category_distribution']}")


if __name__ == "__main__":
    main()
