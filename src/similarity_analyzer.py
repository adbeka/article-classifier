"""
Article similarity analysis using embeddings and cosine similarity.
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class SimilarityAnalyzer:
    """
    Analyzes article similarity using semantic embeddings.
    
    Features:
    - Generate embeddings for articles
    - Calculate similarity between articles
    - Find similar articles in a collection
    - Detect duplicate articles
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the similarity analyzer.
        
        Args:
            model_name: Name of the sentence-transformers model to use
                       (default: all-MiniLM-L6-v2 - fast and efficient)
        """
        logger.info(f"Loading similarity model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        logger.info("Similarity analyzer initialized successfully")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding vector for a text.
        
        Args:
            text: The text to embed
            
        Returns:
            Numpy array representing the embedding
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(384)  # Default embedding size for MiniLM
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_article_embedding(self, article: Dict) -> np.ndarray:
        """
        Generate embedding for an article using title and content.
        
        Args:
            article: Dictionary containing article data
            
        Returns:
            Numpy array representing the article embedding
        """
        # Combine title and content (or summary if content is long)
        title = article.get('title', '')
        content = article.get('content', '')
        summary = article.get('summary', '')
        
        # Use title + summary for better performance, or title + first 1000 chars of content
        if summary:
            text = f"{title}. {summary}"
        else:
            text = f"{title}. {content[:1000]}"
        
        return self.generate_embedding(text)
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        # Handle edge cases
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        # Ensure arrays are numpy arrays
        if not isinstance(embedding1, np.ndarray):
            embedding1 = np.array(embedding1)
        if not isinstance(embedding2, np.ndarray):
            embedding2 = np.array(embedding2)
        
        # Calculate cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def find_similar_articles(
        self, 
        query_article: Dict, 
        article_pool: List[Dict],
        top_k: int = 5,
        min_similarity: float = 0.5
    ) -> List[Dict]:
        """
        Find similar articles from a pool of articles.
        
        Args:
            query_article: The article to find similar articles for
            article_pool: List of articles to search through
            top_k: Maximum number of similar articles to return
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            List of similar articles with similarity scores
        """
        if not article_pool:
            return []
        
        # Generate embedding for query article
        query_embedding = self.generate_article_embedding(query_article)
        
        # Calculate similarities
        similarities = []
        for article in article_pool:
            # Skip if it's the same article (by URL or title)
            if (article.get('url') == query_article.get('url') or 
                article.get('title') == query_article.get('title')):
                continue
            
            # Generate embedding and calculate similarity
            article_embedding = self.generate_article_embedding(article)
            similarity = self.calculate_similarity(query_embedding, article_embedding)
            
            if similarity >= min_similarity:
                similarities.append({
                    'article': article,
                    'similarity_score': similarity
                })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similarities[:top_k]
    
    def is_duplicate(
        self, 
        article1: Dict, 
        article2: Dict, 
        threshold: float = 0.9
    ) -> bool:
        """
        Check if two articles are duplicates based on similarity threshold.
        
        Args:
            article1: First article
            article2: Second article
            threshold: Similarity threshold for duplicate detection (default: 0.9)
            
        Returns:
            True if articles are considered duplicates
        """
        embedding1 = self.generate_article_embedding(article1)
        embedding2 = self.generate_article_embedding(article2)
        similarity = self.calculate_similarity(embedding1, embedding2)
        
        return similarity >= threshold
    
    def find_duplicates_in_batch(
        self, 
        articles: List[Dict],
        threshold: float = 0.9
    ) -> List[Tuple[int, int, float]]:
        """
        Find duplicate articles in a batch.
        
        Args:
            articles: List of articles to check
            threshold: Similarity threshold for duplicate detection
            
        Returns:
            List of tuples (index1, index2, similarity) for duplicate pairs
        """
        if len(articles) < 2:
            return []
        
        # Generate all embeddings first
        embeddings = [self.generate_article_embedding(article) for article in articles]
        
        # Find duplicates
        duplicates = []
        for i in range(len(articles)):
            for j in range(i + 1, len(articles)):
                similarity = self.calculate_similarity(embeddings[i], embeddings[j])
                if similarity >= threshold:
                    duplicates.append((i, j, similarity))
        
        return duplicates
    
    def cluster_similar_articles(
        self,
        articles: List[Dict],
        similarity_threshold: float = 0.7
    ) -> List[List[int]]:
        """
        Group similar articles into clusters.
        
        Args:
            articles: List of articles to cluster
            similarity_threshold: Minimum similarity to be in same cluster
            
        Returns:
            List of clusters, where each cluster is a list of article indices
        """
        if not articles:
            return []
        
        # Generate embeddings
        embeddings = [self.generate_article_embedding(article) for article in articles]
        
        # Simple clustering: greedy approach
        clusters = []
        assigned = set()
        
        for i in range(len(articles)):
            if i in assigned:
                continue
            
            # Start new cluster
            cluster = [i]
            assigned.add(i)
            
            # Find similar articles
            for j in range(i + 1, len(articles)):
                if j in assigned:
                    continue
                
                similarity = self.calculate_similarity(embeddings[i], embeddings[j])
                if similarity >= similarity_threshold:
                    cluster.append(j)
                    assigned.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def analyze_article_similarity(
        self,
        article: Dict,
        reference_articles: List[Dict]
    ) -> Dict:
        """
        Comprehensive similarity analysis for an article.
        
        Args:
            article: The article to analyze
            reference_articles: List of articles to compare against
            
        Returns:
            Dictionary containing similarity analysis results
        """
        if not reference_articles:
            return {
                'has_duplicates': False,
                'duplicate_count': 0,
                'similar_articles': [],
                'max_similarity': 0.0,
                'avg_similarity': 0.0
            }
        
        # Find similar articles
        similar = self.find_similar_articles(
            article, 
            reference_articles, 
            top_k=10, 
            min_similarity=0.3
        )
        
        # Identify duplicates (similarity >= 0.9)
        duplicates = [s for s in similar if s['similarity_score'] >= 0.9]
        
        # Calculate statistics
        similarities = [s['similarity_score'] for s in similar] if similar else [0.0]
        
        return {
            'has_duplicates': len(duplicates) > 0,
            'duplicate_count': len(duplicates),
            'duplicates': [
                {
                    'title': d['article'].get('title', 'Unknown'),
                    'url': d['article'].get('url', ''),
                    'similarity': d['similarity_score']
                }
                for d in duplicates
            ],
            'similar_articles': [
                {
                    'title': s['article'].get('title', 'Unknown'),
                    'url': s['article'].get('url', ''),
                    'category': s['article'].get('classification', {}).get('top_label', 'Unknown'),
                    'similarity': s['similarity_score']
                }
                for s in similar[:5]  # Top 5 similar
            ],
            'max_similarity': max(similarities),
            'avg_similarity': sum(similarities) / len(similarities) if similarities else 0.0,
            'total_similar_found': len(similar)
        }
