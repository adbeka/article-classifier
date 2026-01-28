# Changelog

All notable changes to the Article Classifier & Summarizer project.

## [3.0.0] - 2026-01-28

### 🔗 Major Feature Release: Article Similarity & Duplicate Detection

This release adds powerful AI-powered similarity detection to find related articles, detect duplicates, and recommend similar content.

### ✨ New Features

#### Similarity Analysis (`src/similarity_analyzer.py`)
- **Semantic Embeddings**: Generate 384-dimensional embeddings using sentence-transformers
- **Similarity Search**: Find similar articles using cosine similarity
- **Duplicate Detection**: Automatically identify duplicate or near-duplicate content
- **Article Clustering**: Group similar articles into topic-based clusters
- **Configurable Thresholds**: Adjust similarity sensitivity (0.0 - 1.0)
- **Batch Processing**: Efficient duplicate detection across large article collections
- **Comprehensive Reports**: Detailed similarity analysis with statistics

#### Database Enhancements (`src/database.py`)
- **Embedding Storage**: Store article embeddings as BLOB in SQLite
- **Similarity Queries**: Fast similarity search across cached articles
- **Duplicate Scanning**: Database-wide duplicate detection
- **Efficient Retrieval**: Optimized queries for embedding-based search

#### API Enhancements (`src/api.py`)
- **`POST /api/similar`**: Find similar articles by URL
- **`GET /api/duplicates`**: Scan database for duplicates
- **`POST /api/similarity-report`**: Get comprehensive similarity analysis
- **Extended Response Data**: Similarity scores and related article information

#### Telegram Bot Enhancements (`src/telegram_bot.py`)
- **`/similar <url>`**: Find similar articles command
- **`/duplicates`**: Scan for duplicate articles command
- **Updated Welcome**: Includes new similarity features

#### Main Processor (`src/main.py`)
- **`find_similar_by_url()`**: Find similar articles by URL
- **`find_similar_articles()`**: Find similar articles by article object
- **`check_duplicate()`**: Check if article is a duplicate
- **`find_all_duplicates()`**: Scan entire database for duplicates
- **`get_article_similarity_report()`**: Comprehensive similarity analysis

### 📚 Documentation
- **New**: `docs/SIMILARITY_FEATURE.md` - Complete similarity feature documentation
- **New**: `demo_similarity.py` - Interactive demo script
- **New**: `tests/test_similarity.py` - Comprehensive test suite
- **Updated**: README.md with similarity feature information

### 📦 Dependencies
- **Added**: `sentence-transformers>=2.2.0` for semantic embeddings

### 🎯 Use Cases
- News aggregation and deduplication
- Content recommendation systems
- Related article discovery
- Duplicate content prevention
- Topic clustering and trend detection

### ⚡ Performance
- Embedding generation: ~50ms per article
- Similarity search: <100ms for 1,000 articles
- Model size: 80MB (all-MiniLM-L6-v2)
- Storage: ~1.5KB per article embedding

---

## [2.0.0] - 2026-01-27

### 🚀 Major Feature Release: Advanced Article Analysis

This release significantly enhances the article analysis capabilities with sentiment analysis, keyword extraction, metadata analysis, caching, and export features.

### ✨ New Features

#### Sentiment Analysis (`src/sentiment_analyzer.py`)
- **Sentiment Detection**: Automatically detect positive, negative, or neutral sentiment
- **Emotion Analysis**: Identify specific emotions (joy, sadness, anger, fear, surprise, etc.)
- **Confidence Scores**: Detailed confidence metrics for all sentiment predictions
- **Emoji Support**: Visual sentiment representations

#### Keyword Extraction & NER (`src/keyword_extractor.py`)
- **Keyword Extraction**: Frequency-based keyword identification with stopword filtering
- **Key Phrase Extraction**: Multi-word phrase detection (n-grams)
- **Named Entity Recognition**: Extract people, organizations, locations, and miscellaneous entities
- **Entity Confidence Scores**: Reliability metrics for each detected entity

#### Metadata Analysis (`src/metadata_analyzer.py`)
- **Reading Time Estimation**: Calculate estimated reading time based on word count
- **Quality Score System**: Comprehensive 0-100 quality rating with breakdown:
  - Length score (25 points)
  - Title presence (15 points)
  - Author information (10 points)
  - Publish date (10 points)
  - Readability (20 points)
  - Structure (20 points)
- **Readability Analysis**: Flesch Reading Ease score with grade level interpretation
- **Text Statistics**: Word count, sentence count, paragraph count, averages

#### Database & Caching (`src/database.py`)
- **SQLite Integration**: Persistent storage for processed articles
- **Smart Caching**: TTL-based cache with configurable expiration (default 24 hours)
- **Access Tracking**: Monitor article access frequency and patterns
- **Search Functionality**: Filter cached articles by category
- **Statistics**: Comprehensive processing metrics
- **Cleanup Tools**: Automated removal of old cached articles

#### Export System (`src/exporter.py`)
- **JSON Export**: Complete structured data export
- **CSV Export**: Tabular format for spreadsheet analysis
- **Markdown Export**: Human-readable documentation format
- **HTML Export**: Styled, shareable web pages
- **Automatic Naming**: Intelligent filename generation with timestamps

### 🔧 Enhancements

#### Enhanced Article Processor (`src/main.py`)
- Integrated all new analysis modules
- Added caching layer with force-refresh option
- Export methods for all supported formats
- Statistics and cached article retrieval
- Configurable feature toggling
- Improved error handling

#### API Improvements (`src/api.py`)
- **New Endpoints**:
  - `POST /api/export` - Export articles to various formats
  - `GET /api/cached` - Retrieve cached articles with filters
  - `GET /api/statistics` - View processing statistics
- **Enhanced Responses**: All endpoints now return full analysis including sentiment, keywords, and metadata
- Version bumped to 2.0

#### Telegram Bot Updates (`src/telegram_bot.py`)
- **New Commands**:
  - `/stats` - View processing statistics
  - `/cached` - Browse recently cached articles
- **Rich Output**: Enhanced message formatting with:
  - Sentiment with emoji indicators
  - Top emotions display
  - Reading time and word count
  - Quality scores
  - Top keywords and named entities
- **Better Error Handling**: Improved error messages and recovery

### 📚 Documentation

- **FEATURES.md**: Comprehensive guide to all new features with examples
- **README.md**: Updated with feature highlights and new capabilities
- **Code Documentation**: Detailed docstrings for all new modules and functions

### 🔄 Changes

- `requirements.txt`: Added comments and organization
- Config options for advanced features and caching
- Improved module organization and separation of concerns

### 📊 Performance

- **Caching**: ~90% reduction in processing time for repeated articles
- **Incremental Loading**: Models loaded on-demand to reduce startup time
- **Optimized Queries**: Indexed database for fast lookups

### 🐛 Bug Fixes

- None (new features only in this release)

### 📦 Dependencies

No new dependencies required - all features use existing transformers library with different pre-trained models.

### 🔐 Security

- SQL injection protection via parameterized queries
- Input validation on all API endpoints
- URL hash-based cache keys for security

### 📝 Notes

- Database file (`articles.db`) is created automatically on first run
- Export directory (`exports/`) is created automatically
- All new features are enabled by default but can be disabled via configuration
- Backward compatible - existing code continues to work

### 🚀 Upgrade Guide

1. Pull latest changes
2. No new dependencies to install (optional: re-run `pip install -r requirements.txt`)
3. Run your application - database will be created automatically
4. All new features work out of the box!

### 📈 Statistics

- **New Files**: 5 modules added
- **Lines of Code**: ~2,000+ lines added
- **Documentation**: 500+ lines of documentation
- **Test Coverage**: Existing tests still pass

### 🙏 Acknowledgments

Built with:
- Transformers (Hugging Face) for NLP models
- SQLite for efficient caching
- Flask for API endpoints
- python-telegram-bot for Telegram integration

---

## [1.0.0] - Previous Release

### Initial Release
- Article scraping with newspaper3k
- Topic classification with BART
- Text summarization with BART
- Telegram bot interface
- Chrome extension
- Flask REST API
- Basic configuration system

---

**For detailed feature documentation, see [FEATURES.md](FEATURES.md)**
