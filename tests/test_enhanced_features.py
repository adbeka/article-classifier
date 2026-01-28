"""
Tests for new enhanced features: sentiment analysis, keyword extraction, and metadata analysis.
"""
import pytest
from src.sentiment_analyzer import SentimentAnalyzer
from src.keyword_extractor import KeywordExtractor
from src.metadata_analyzer import MetadataAnalyzer
from src.database import ArticleDatabase
from src.exporter import ArticleExporter
import os


class TestSentimentAnalyzer:
    """Test sentiment analysis functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = SentimentAnalyzer()
        self.positive_text = "This is an amazing and wonderful day! I'm so happy and excited about the great news."
        self.negative_text = "This is terrible and awful. I'm very disappointed and sad about this tragic situation."
        self.neutral_text = "The meeting is scheduled for tomorrow at 3 PM in the conference room."
    
    def test_analyze_sentiment_positive(self):
        """Test positive sentiment detection."""
        result = self.analyzer.analyze_sentiment(self.positive_text)
        assert result['label'] == 'POSITIVE'
        assert result['score'] > 0.5
    
    def test_analyze_sentiment_negative(self):
        """Test negative sentiment detection."""
        result = self.analyzer.analyze_sentiment(self.negative_text)
        assert result['label'] == 'NEGATIVE'
        assert result['score'] > 0.5
    
    def test_analyze_sentiment_neutral(self):
        """Test neutral sentiment detection."""
        result = self.analyzer.analyze_sentiment(self.neutral_text)
        assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
        assert 0 <= result['score'] <= 1
    
    def test_analyze_article(self):
        """Test article sentiment analysis."""
        article = {
            'title': 'Great News',
            'text': self.positive_text
        }
        result = self.analyzer.analyze_article(article)
        assert 'sentiment_analysis' in result
        assert 'sentiment' in result['sentiment_analysis']
        assert 'emotions' in result['sentiment_analysis']
    
    def test_get_sentiment_emoji(self):
        """Test emoji mapping."""
        assert self.analyzer.get_sentiment_emoji('POSITIVE') == '😊'
        assert self.analyzer.get_sentiment_emoji('NEGATIVE') == '😞'
        assert self.analyzer.get_sentiment_emoji('NEUTRAL') == '😐'


class TestKeywordExtractor:
    """Test keyword extraction functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.extractor = KeywordExtractor()
        self.sample_text = """
        Artificial intelligence and machine learning are transforming technology.
        Machine learning algorithms use artificial intelligence to learn patterns.
        Technology companies are investing heavily in artificial intelligence research.
        """
    
    def test_extract_keywords_frequency(self):
        """Test frequency-based keyword extraction."""
        keywords = self.extractor.extract_keywords_frequency(self.sample_text, top_n=5)
        assert len(keywords) <= 5
        assert all('word' in kw and 'frequency' in kw for kw in keywords)
        # Check that stopwords are filtered
        words = [kw['word'] for kw in keywords]
        assert 'the' not in words
        assert 'and' not in words
    
    def test_extract_key_phrases(self):
        """Test key phrase extraction."""
        phrases = self.extractor.extract_key_phrases(self.sample_text, top_n=5)
        assert isinstance(phrases, list)
        for phrase in phrases:
            assert 'phrase' in phrase
            assert 'frequency' in phrase
            assert phrase['frequency'] > 1
    
    def test_analyze_article(self):
        """Test article keyword analysis."""
        article = {
            'title': 'AI Technology',
            'text': self.sample_text
        }
        result = self.extractor.analyze_article(article)
        assert 'keyword_analysis' in result
        assert 'keywords' in result['keyword_analysis']
        assert 'key_phrases' in result['keyword_analysis']


class TestMetadataAnalyzer:
    """Test metadata analysis functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = MetadataAnalyzer()
        self.sample_text = " ".join(["word"] * 400)  # 400 words
    
    def test_calculate_reading_time(self):
        """Test reading time calculation."""
        result = self.analyzer.calculate_reading_time(self.sample_text)
        assert 'minutes' in result
        assert 'formatted' in result
        assert 'word_count' in result
        assert result['word_count'] == 400
        assert result['minutes'] == 2  # 400 words / 200 wpm = 2 minutes
    
    def test_calculate_reading_time_short(self):
        """Test reading time for short text."""
        short_text = "Short text"
        result = self.analyzer.calculate_reading_time(short_text)
        assert result['minutes'] == 1
        assert 'Less than' in result['formatted']
    
    def test_count_syllables(self):
        """Test syllable counting."""
        assert self.analyzer._count_syllables('hello') == 2
        assert self.analyzer._count_syllables('beautiful') == 3
        assert self.analyzer._count_syllables('cat') == 1
    
    def test_calculate_readability_score(self):
        """Test readability score calculation."""
        text = "This is a simple sentence. It has easy words. Anyone can read this."
        result = self.analyzer.calculate_readability_score(text)
        assert 'score' in result
        assert 'interpretation' in result
        assert 'grade_level' in result
        assert 0 <= result['score'] <= 100
    
    def test_get_text_statistics(self):
        """Test text statistics."""
        text = "This is a test. It has two sentences."
        stats = self.analyzer.get_text_statistics(text)
        assert stats['word_count'] == 8
        assert stats['sentence_count'] == 2
        assert stats['paragraph_count'] >= 1
        assert 'average_word_length' in stats
        assert 'average_sentence_length' in stats
    
    def test_calculate_quality_score(self):
        """Test quality score calculation."""
        article = {
            'title': 'Test Article Title',
            'text': self.sample_text,
            'authors': ['John Doe'],
            'publish_date': '2024-01-01'
        }
        result = self.analyzer.calculate_quality_score(article)
        assert 'score' in result
        assert 'grade' in result
        assert 'breakdown' in result
        assert 0 <= result['score'] <= 100
    
    def test_analyze_article(self):
        """Test complete article metadata analysis."""
        article = {
            'title': 'Test Article',
            'text': self.sample_text,
            'authors': ['John Doe'],
            'publish_date': '2024-01-01'
        }
        result = self.analyzer.analyze_article(article)
        assert 'metadata_analysis' in result
        metadata = result['metadata_analysis']
        assert 'reading_time' in metadata
        assert 'readability' in metadata
        assert 'quality_score' in metadata
        assert 'text_statistics' in metadata


class TestArticleDatabase:
    """Test database functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.test_db_path = "test_articles.db"
        self.db = ArticleDatabase(self.test_db_path)
        self.sample_article = {
            'url': 'https://example.com/test-article',
            'title': 'Test Article',
            'text': 'This is a test article.',
            'authors': ['Test Author'],
            'publish_date': '2024-01-01',
            'classification': {'top_label': 'technology', 'top_score': 0.95},
            'summary': 'Test summary',
            'sentiment_analysis': {'sentiment': {'label': 'POSITIVE', 'score': 0.9}},
            'keyword_analysis': {'keywords': [], 'entities': []},
            'metadata_analysis': {'reading_time': {'minutes': 1}}
        }
    
    def teardown_method(self):
        """Cleanup test database."""
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_save_article(self):
        """Test saving an article."""
        article_id = self.db.save_article(self.sample_article)
        assert article_id is not None
        assert article_id > 0
    
    def test_get_article(self):
        """Test retrieving a cached article."""
        # Save first
        self.db.save_article(self.sample_article)
        
        # Retrieve
        cached = self.db.get_article(self.sample_article['url'])
        assert cached is not None
        assert cached['title'] == self.sample_article['title']
        assert cached['url'] == self.sample_article['url']
    
    def test_search_articles(self):
        """Test searching articles."""
        # Save multiple articles
        self.db.save_article(self.sample_article)
        
        article2 = self.sample_article.copy()
        article2['url'] = 'https://example.com/test-article-2'
        self.db.save_article(article2)
        
        # Search
        results = self.db.search_articles(limit=10)
        assert len(results) >= 2
    
    def test_get_statistics(self):
        """Test getting statistics."""
        self.db.save_article(self.sample_article)
        
        stats = self.db.get_statistics()
        assert 'total_articles' in stats
        assert stats['total_articles'] >= 1
        assert 'category_distribution' in stats


class TestArticleExporter:
    """Test export functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.test_export_dir = "test_exports"
        self.exporter = ArticleExporter(self.test_export_dir)
        self.sample_article = {
            'url': 'https://example.com/test',
            'title': 'Test Article',
            'text': 'This is test content.',
            'summary': 'Test summary',
            'classification': {'top_label': 'technology', 'top_score': 0.95},
            'sentiment_analysis': {'sentiment': {'label': 'POSITIVE', 'score': 0.9}},
            'keyword_analysis': {'keywords': [], 'entities': []},
            'metadata_analysis': {'reading_time': {'formatted': '1 minute'}}
        }
    
    def teardown_method(self):
        """Cleanup test exports."""
        import shutil
        if os.path.exists(self.test_export_dir):
            shutil.rmtree(self.test_export_dir)
    
    def test_export_to_json(self):
        """Test JSON export."""
        filepath = self.exporter.export_to_json(self.sample_article)
        assert os.path.exists(filepath)
        assert filepath.endswith('.json')
    
    def test_export_to_markdown(self):
        """Test Markdown export."""
        filepath = self.exporter.export_to_markdown(self.sample_article)
        assert os.path.exists(filepath)
        assert filepath.endswith('.md')
    
    def test_export_to_html(self):
        """Test HTML export."""
        filepath = self.exporter.export_to_html(self.sample_article)
        assert os.path.exists(filepath)
        assert filepath.endswith('.html')
    
    def test_export_to_csv(self):
        """Test CSV export."""
        articles = [self.sample_article]
        filepath = self.exporter.export_to_csv(articles)
        assert os.path.exists(filepath)
        assert filepath.endswith('.csv')
    
    def test_slugify(self):
        """Test filename slugification."""
        slug = self.exporter._slugify("Test Article Title!")
        assert slug == "test-article-title"
        assert ' ' not in slug
        assert '!' not in slug


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
