"""
Database storage module for caching processed articles.
"""
import sqlite3
import json
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import hashlib
from pathlib import Path


class ArticleDatabase:
    """Database for storing and caching processed articles."""
    
    def __init__(self, db_path: str = "articles.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize the database schema."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        
        cursor = self.conn.cursor()
        
        # Create articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                url_hash TEXT UNIQUE NOT NULL,
                title TEXT,
                text TEXT,
                authors TEXT,
                publish_date TEXT,
                top_image TEXT,
                classification TEXT,
                summary TEXT,
                sentiment_analysis TEXT,
                keyword_analysis TEXT,
                metadata_analysis TEXT,
                processed_at TEXT NOT NULL,
                access_count INTEGER DEFAULT 1,
                last_accessed TEXT NOT NULL
            )
        ''')
        
        # Create indexes for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_url_hash ON articles(url_hash)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_processed_at ON articles(processed_at)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_classification ON articles(classification)
        ''')
        
        self.conn.commit()
    
    def _hash_url(self, url: str) -> str:
        """
        Create a hash of the URL for faster lookups.
        
        Args:
            url: The article URL
            
        Returns:
            SHA256 hash of the URL
        """
        return hashlib.sha256(url.encode()).hexdigest()
    
    def save_article(self, article: Dict[str, any]) -> int:
        """
        Save a processed article to the database.
        
        Args:
            article: Article dictionary with all processed data
            
        Returns:
            ID of the saved article
        """
        cursor = self.conn.cursor()
        url = article.get('url', '')
        url_hash = self._hash_url(url)
        now = datetime.utcnow().isoformat()
        
        # Serialize complex fields to JSON
        classification = json.dumps(article.get('classification', {}))
        sentiment_analysis = json.dumps(article.get('sentiment_analysis', {}))
        keyword_analysis = json.dumps(article.get('keyword_analysis', {}))
        metadata_analysis = json.dumps(article.get('metadata_analysis', {}))
        authors = json.dumps(article.get('authors', []))
        
        try:
            cursor.execute('''
                INSERT INTO articles (
                    url, url_hash, title, text, authors, publish_date, top_image,
                    classification, summary, sentiment_analysis, keyword_analysis,
                    metadata_analysis, processed_at, last_accessed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                url,
                url_hash,
                article.get('title'),
                article.get('text'),
                authors,
                article.get('publish_date'),
                article.get('top_image'),
                classification,
                article.get('summary'),
                sentiment_analysis,
                keyword_analysis,
                metadata_analysis,
                now,
                now
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Article already exists, update it
            return self.update_article(article)
    
    def update_article(self, article: Dict[str, any]) -> int:
        """
        Update an existing article in the database.
        
        Args:
            article: Article dictionary with updated data
            
        Returns:
            ID of the updated article
        """
        cursor = self.conn.cursor()
        url = article.get('url', '')
        url_hash = self._hash_url(url)
        now = datetime.utcnow().isoformat()
        
        # Serialize complex fields to JSON
        classification = json.dumps(article.get('classification', {}))
        sentiment_analysis = json.dumps(article.get('sentiment_analysis', {}))
        keyword_analysis = json.dumps(article.get('keyword_analysis', {}))
        metadata_analysis = json.dumps(article.get('metadata_analysis', {}))
        authors = json.dumps(article.get('authors', []))
        
        cursor.execute('''
            UPDATE articles SET
                title = ?,
                text = ?,
                authors = ?,
                publish_date = ?,
                top_image = ?,
                classification = ?,
                summary = ?,
                sentiment_analysis = ?,
                keyword_analysis = ?,
                metadata_analysis = ?,
                processed_at = ?,
                access_count = access_count + 1,
                last_accessed = ?
            WHERE url_hash = ?
        ''', (
            article.get('title'),
            article.get('text'),
            authors,
            article.get('publish_date'),
            article.get('top_image'),
            classification,
            article.get('summary'),
            sentiment_analysis,
            keyword_analysis,
            metadata_analysis,
            now,
            now,
            url_hash
        ))
        self.conn.commit()
        
        # Get the article ID
        cursor.execute('SELECT id FROM articles WHERE url_hash = ?', (url_hash,))
        result = cursor.fetchone()
        return result['id'] if result else None
    
    def get_article(self, url: str, max_age_hours: int = 24) -> Optional[Dict[str, any]]:
        """
        Retrieve a cached article from the database.
        
        Args:
            url: The article URL
            max_age_hours: Maximum age of cached article in hours (default 24)
            
        Returns:
            Article dictionary if found and not expired, None otherwise
        """
        cursor = self.conn.cursor()
        url_hash = self._hash_url(url)
        
        # Calculate expiry time
        expiry_time = (datetime.utcnow() - timedelta(hours=max_age_hours)).isoformat()
        
        cursor.execute('''
            SELECT * FROM articles
            WHERE url_hash = ? AND processed_at > ?
        ''', (url_hash, expiry_time))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # Update access count and last accessed time
        now = datetime.utcnow().isoformat()
        cursor.execute('''
            UPDATE articles
            SET access_count = access_count + 1, last_accessed = ?
            WHERE id = ?
        ''', (now, row['id']))
        self.conn.commit()
        
        # Convert row to dictionary and deserialize JSON fields
        article = dict(row)
        article['authors'] = json.loads(article['authors'])
        article['classification'] = json.loads(article['classification'])
        article['sentiment_analysis'] = json.loads(article['sentiment_analysis'])
        article['keyword_analysis'] = json.loads(article['keyword_analysis'])
        article['metadata_analysis'] = json.loads(article['metadata_analysis'])
        
        return article
    
    def search_articles(self, 
                       category: Optional[str] = None,
                       limit: int = 10,
                       offset: int = 0) -> List[Dict[str, any]]:
        """
        Search articles by category or other criteria.
        
        Args:
            category: Filter by classification category
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of article dictionaries
        """
        cursor = self.conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT * FROM articles
                WHERE classification LIKE ?
                ORDER BY processed_at DESC
                LIMIT ? OFFSET ?
            ''', (f'%"{category}"%', limit, offset))
        else:
            cursor.execute('''
                SELECT * FROM articles
                ORDER BY processed_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
        
        rows = cursor.fetchall()
        
        articles = []
        for row in rows:
            article = dict(row)
            article['authors'] = json.loads(article['authors'])
            article['classification'] = json.loads(article['classification'])
            article['sentiment_analysis'] = json.loads(article['sentiment_analysis'])
            article['keyword_analysis'] = json.loads(article['keyword_analysis'])
            article['metadata_analysis'] = json.loads(article['metadata_analysis'])
            articles.append(article)
        
        return articles
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()
        
        # Total articles
        cursor.execute('SELECT COUNT(*) as count FROM articles')
        total_articles = cursor.fetchone()['count']
        
        # Articles by category
        cursor.execute('SELECT classification FROM articles')
        classifications = []
        for row in cursor.fetchall():
            try:
                classification = json.loads(row['classification'])
                if 'top_label' in classification:
                    classifications.append(classification['top_label'])
            except (json.JSONDecodeError, KeyError):
                pass
        
        category_counts = {}
        for cat in classifications:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Most accessed articles
        cursor.execute('''
            SELECT url, title, access_count
            FROM articles
            ORDER BY access_count DESC
            LIMIT 5
        ''')
        top_articles = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_articles': total_articles,
            'category_distribution': category_counts,
            'top_articles': top_articles
        }
    
    def clear_old_articles(self, days: int = 30) -> int:
        """
        Delete articles older than specified days.
        
        Args:
            days: Delete articles older than this many days
            
        Returns:
            Number of articles deleted
        """
        cursor = self.conn.cursor()
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        cursor.execute('DELETE FROM articles WHERE processed_at < ?', (cutoff_date,))
        deleted_count = cursor.rowcount
        self.conn.commit()
        
        return deleted_count
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
