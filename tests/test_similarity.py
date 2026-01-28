"""
Unit tests for similarity analyzer functionality.
"""
import unittest
import numpy as np
from src.similarity_analyzer import SimilarityAnalyzer


class TestSimilarityAnalyzer(unittest.TestCase):
    """Test cases for SimilarityAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SimilarityAnalyzer()
        
        # Sample articles for testing
        self.article1 = {
            'title': 'Artificial Intelligence Revolutionizes Healthcare',
            'content': 'Machine learning and AI are transforming medical diagnosis and treatment.',
            'summary': 'AI and machine learning are improving healthcare outcomes.',
            'url': 'https://example.com/ai-healthcare'
        }
        
        self.article2 = {
            'title': 'AI in Medicine: A New Era',
            'content': 'Artificial intelligence is changing how doctors diagnose and treat patients.',
            'summary': 'AI is revolutionizing medical practice and patient care.',
            'url': 'https://example.com/ai-medicine'
        }
        
        self.article3 = {
            'title': 'Football Championship Finals 2026',
            'content': 'The championship game saw an exciting finish with a last-minute goal.',
            'summary': 'Sports fans witnessed an thrilling championship match.',
            'url': 'https://example.com/sports-finals'
        }
    
    def test_generate_embedding(self):
        """Test embedding generation."""
        text = "This is a test sentence for embedding generation."
        embedding = self.analyzer.generate_embedding(text)
        
        # Check that embedding is a numpy array
        self.assertIsInstance(embedding, np.ndarray)
        
        # Check embedding dimension (384 for MiniLM model)
        self.assertEqual(len(embedding), 384)
        
        # Check that embedding is not all zeros
        self.assertNotEqual(np.sum(embedding), 0)
    
    def test_generate_embedding_empty_text(self):
        """Test embedding generation with empty text."""
        embedding = self.analyzer.generate_embedding("")
        
        # Should return zero vector
        self.assertIsInstance(embedding, np.ndarray)
        self.assertEqual(np.sum(embedding), 0)
    
    def test_generate_article_embedding(self):
        """Test article embedding generation."""
        embedding = self.analyzer.generate_article_embedding(self.article1)
        
        # Check that embedding is generated
        self.assertIsInstance(embedding, np.ndarray)
        self.assertEqual(len(embedding), 384)
    
    def test_calculate_similarity_identical(self):
        """Test similarity calculation for identical embeddings."""
        embedding = self.analyzer.generate_embedding("Test text")
        similarity = self.analyzer.calculate_similarity(embedding, embedding)
        
        # Identical embeddings should have similarity close to 1.0
        self.assertAlmostEqual(similarity, 1.0, places=5)
    
    def test_calculate_similarity_different(self):
        """Test similarity calculation for different texts."""
        embedding1 = self.analyzer.generate_embedding("Artificial intelligence in healthcare")
        embedding2 = self.analyzer.generate_embedding("Sports championship football game")
        
        similarity = self.analyzer.calculate_similarity(embedding1, embedding2)
        
        # Different topics should have lower similarity
        self.assertLess(similarity, 0.5)
    
    def test_calculate_similarity_similar(self):
        """Test similarity calculation for similar texts."""
        embedding1 = self.analyzer.generate_embedding("Machine learning in medical diagnosis")
        embedding2 = self.analyzer.generate_embedding("AI for healthcare and medicine")
        
        similarity = self.analyzer.calculate_similarity(embedding1, embedding2)
        
        # Similar topics should have higher similarity
        self.assertGreater(similarity, 0.5)
    
    def test_find_similar_articles(self):
        """Test finding similar articles."""
        article_pool = [self.article1, self.article2, self.article3]
        
        # Find articles similar to article1
        similar = self.analyzer.find_similar_articles(
            self.article1,
            article_pool,
            top_k=2,
            min_similarity=0.3
        )
        
        # Should find article2 as similar (both about AI in healthcare)
        self.assertGreater(len(similar), 0)
        
        # Most similar should be article2
        most_similar = similar[0]
        self.assertEqual(most_similar['article']['url'], self.article2['url'])
        
        # Similarity should be high
        self.assertGreater(most_similar['similarity_score'], 0.5)
    
    def test_find_similar_articles_no_matches(self):
        """Test finding similar articles with high threshold."""
        article_pool = [self.article3]  # Only sports article
        
        similar = self.analyzer.find_similar_articles(
            self.article1,  # AI healthcare article
            article_pool,
            top_k=5,
            min_similarity=0.8  # High threshold
        )
        
        # Should find no similar articles
        self.assertEqual(len(similar), 0)
    
    def test_is_duplicate(self):
        """Test duplicate detection."""
        # Test with identical content (different URLs)
        article_copy = self.article1.copy()
        article_copy['url'] = 'https://example.com/duplicate'
        
        is_dup = self.analyzer.is_duplicate(self.article1, article_copy, threshold=0.95)
        
        # Should be detected as duplicate
        self.assertTrue(is_dup)
    
    def test_is_not_duplicate(self):
        """Test non-duplicate detection."""
        is_dup = self.analyzer.is_duplicate(
            self.article1,  # AI article
            self.article3,  # Sports article
            threshold=0.9
        )
        
        # Should not be detected as duplicate
        self.assertFalse(is_dup)
    
    def test_find_duplicates_in_batch(self):
        """Test batch duplicate detection."""
        # Create a duplicate of article1
        article1_dup = self.article1.copy()
        article1_dup['url'] = 'https://example.com/duplicate-ai'
        
        articles = [self.article1, article1_dup, self.article2, self.article3]
        
        duplicates = self.analyzer.find_duplicates_in_batch(articles, threshold=0.95)
        
        # Should find at least one duplicate pair
        self.assertGreater(len(duplicates), 0)
        
        # Check duplicate indices and similarity
        for idx1, idx2, similarity in duplicates:
            self.assertNotEqual(idx1, idx2)
            self.assertGreaterEqual(similarity, 0.95)
    
    def test_cluster_similar_articles(self):
        """Test article clustering."""
        # Create articles with clear topics
        articles = [
            self.article1,  # AI healthcare
            self.article2,  # AI medicine (similar to article1)
            self.article3   # Sports (different)
        ]
        
        clusters = self.analyzer.cluster_similar_articles(
            articles,
            similarity_threshold=0.5
        )
        
        # Should create at least 2 clusters (AI articles and sports)
        self.assertGreaterEqual(len(clusters), 2)
        
        # Each cluster should have at least one article
        for cluster in clusters:
            self.assertGreater(len(cluster), 0)
    
    def test_analyze_article_similarity(self):
        """Test comprehensive similarity analysis."""
        reference_articles = [self.article2, self.article3]
        
        analysis = self.analyzer.analyze_article_similarity(
            self.article1,
            reference_articles
        )
        
        # Check analysis structure
        self.assertIn('has_duplicates', analysis)
        self.assertIn('similar_articles', analysis)
        self.assertIn('max_similarity', analysis)
        self.assertIn('avg_similarity', analysis)
        
        # Should find article2 as similar
        self.assertGreater(len(analysis['similar_articles']), 0)
        
        # Check similarity scores
        self.assertGreater(analysis['max_similarity'], 0)
        self.assertGreaterEqual(analysis['avg_similarity'], 0)
    
    def test_analyze_article_similarity_empty_references(self):
        """Test similarity analysis with no reference articles."""
        analysis = self.analyzer.analyze_article_similarity(
            self.article1,
            []
        )
        
        # Should return default structure
        self.assertFalse(analysis['has_duplicates'])
        self.assertEqual(analysis['duplicate_count'], 0)
        self.assertEqual(len(analysis['similar_articles']), 0)
        self.assertEqual(analysis['max_similarity'], 0.0)
    
    def test_calculate_similarity_with_none(self):
        """Test similarity calculation with None values."""
        embedding = self.analyzer.generate_embedding("Test")
        
        similarity = self.analyzer.calculate_similarity(None, embedding)
        self.assertEqual(similarity, 0.0)
        
        similarity = self.analyzer.calculate_similarity(embedding, None)
        self.assertEqual(similarity, 0.0)
    
    def test_calculate_similarity_zero_vectors(self):
        """Test similarity calculation with zero vectors."""
        zero_vec = np.zeros(384)
        embedding = self.analyzer.generate_embedding("Test")
        
        similarity = self.analyzer.calculate_similarity(zero_vec, embedding)
        self.assertEqual(similarity, 0.0)


class TestSimilarityIntegration(unittest.TestCase):
    """Integration tests for similarity functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SimilarityAnalyzer()
    
    def test_end_to_end_similarity_workflow(self):
        """Test complete similarity detection workflow."""
        # Create test articles
        articles = [
            {
                'title': 'Climate Change Impact on Agriculture',
                'content': 'Global warming affects crop yields and farming practices.',
                'summary': 'Climate change impacts agricultural productivity.'
            },
            {
                'title': 'Farming Under Climate Crisis',
                'content': 'Agriculture faces challenges from changing weather patterns.',
                'summary': 'Farmers adapt to climate change effects.'
            },
            {
                'title': 'New Smartphone Release 2026',
                'content': 'Tech company announces latest mobile device with advanced features.',
                'summary': 'New smartphone with cutting-edge technology.'
            }
        ]
        
        # Generate embeddings
        for article in articles:
            article['embedding'] = self.analyzer.generate_article_embedding(article)
        
        # Find similar articles to first one
        similar = self.analyzer.find_similar_articles(
            articles[0],
            articles[1:],
            top_k=2,
            min_similarity=0.3
        )
        
        # Should find agriculture article as most similar
        self.assertGreater(len(similar), 0)
        
        # Verify results
        most_similar = similar[0]
        self.assertIn('climate', most_similar['article']['content'].lower())
        self.assertGreater(most_similar['similarity_score'], 0.4)


if __name__ == '__main__':
    unittest.main()
