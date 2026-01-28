# New Features Guide 🚀

This document describes the enhanced features added to the Article Classifier & Summarizer.

## Table of Contents
- [Sentiment Analysis](#sentiment-analysis)
- [Keyword Extraction & Named Entity Recognition](#keyword-extraction--named-entity-recognition)
- [Metadata Analysis](#metadata-analysis)
- [Database Caching](#database-caching)
- [Export Functionality](#export-functionality)
- [API Enhancements](#api-enhancements)
- [Telegram Bot Enhancements](#telegram-bot-enhancements)

---

## Sentiment Analysis

### Overview
Automatically detect the emotional tone and sentiment of articles.

### Features
- **Sentiment Detection**: Classifies articles as POSITIVE, NEGATIVE, or NEUTRAL
- **Emotion Analysis**: Identifies specific emotions (joy, sadness, anger, fear, surprise, etc.)
- **Confidence Scores**: Provides confidence levels for each sentiment/emotion

### Usage

```python
from src.main import ArticleProcessor

processor = ArticleProcessor()
result = processor.process_url("https://example.com/article")

# Access sentiment analysis
sentiment = result['sentiment_analysis']['sentiment']
print(f"Sentiment: {sentiment['label']} ({sentiment['score']*100:.1f}%)")

# Access emotions
emotions = result['sentiment_analysis']['emotions']
for emotion in emotions:
    print(f"{emotion['label']}: {emotion['score']*100:.1f}%")
```

### API Endpoint
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

The response includes:
```json
{
  "sentiment_analysis": {
    "sentiment": {
      "label": "POSITIVE",
      "score": 0.95
    },
    "emotions": [
      {"label": "joy", "score": 0.85},
      {"label": "optimism", "score": 0.72}
    ]
  }
}
```

---

## Keyword Extraction & Named Entity Recognition

### Overview
Extract important keywords, phrases, and named entities from articles.

### Features
- **Keyword Extraction**: Identifies most frequent meaningful words
- **Key Phrase Extraction**: Finds important multi-word phrases
- **Named Entity Recognition (NER)**: Detects people, organizations, locations
- **Entity Types**: PER (Person), ORG (Organization), LOC (Location), MISC (Miscellaneous)

### Usage

```python
result = processor.process_url("https://example.com/article")

# Access keywords
keywords = result['keyword_analysis']['keywords']
for kw in keywords[:10]:
    print(f"{kw['word']}: {kw['frequency']} occurrences")

# Access named entities
entities = result['keyword_analysis']['entities']
for entity in entities:
    print(f"{entity['text']} ({entity['type']}) - confidence: {entity['score']}")

# Access key phrases
phrases = result['keyword_analysis']['key_phrases']
for phrase in phrases:
    print(f"{phrase['phrase']}: {phrase['frequency']} times")
```

### Example Output
```
Keywords: technology (15), innovation (12), artificial (10)
Entities: 
  - Elon Musk (PER) - 0.995
  - Tesla (ORG) - 0.987
  - California (LOC) - 0.923
Key Phrases: artificial intelligence, machine learning, neural networks
```

---

## Metadata Analysis

### Overview
Calculate comprehensive metadata about articles including reading time, quality score, and readability.

### Features
1. **Reading Time Estimation**
   - Calculates based on average adult reading speed (200 words/minute)
   - Formatted output (e.g., "5 minutes read")

2. **Quality Score (0-100)**
   - Length score (25 points)
   - Title presence (15 points)
   - Author information (10 points)
   - Publish date (10 points)
   - Readability score (20 points)
   - Structure score (20 points)

3. **Readability Analysis**
   - Flesch Reading Ease score
   - Grade level interpretation
   - Difficulty assessment

4. **Text Statistics**
   - Word count
   - Sentence count
   - Paragraph count
   - Character count
   - Average word/sentence length

### Usage

```python
result = processor.process_url("https://example.com/article")

metadata = result['metadata_analysis']

# Reading time
print(f"Reading Time: {metadata['reading_time']['formatted']}")
print(f"Word Count: {metadata['reading_time']['word_count']}")

# Quality score
quality = metadata['quality_score']
print(f"Quality: {quality['score']}/100 ({quality['grade']})")
print(f"Breakdown: {quality['breakdown']}")

# Readability
readability = metadata['readability']
print(f"Readability: {readability['interpretation']}")
print(f"Grade Level: {readability['grade_level']}")

# Statistics
stats = metadata['text_statistics']
print(f"Words: {stats['word_count']}")
print(f"Sentences: {stats['sentence_count']}")
print(f"Paragraphs: {stats['paragraph_count']}")
```

### Quality Score Interpretation
- **90-100**: Excellent - Well-structured, comprehensive article
- **80-89**: Very Good - High-quality content
- **70-79**: Good - Solid article with minor issues
- **60-69**: Fair - Acceptable but could be improved
- **<60**: Poor - Significant quality issues

---

## Database Caching

### Overview
SQLite-based caching system to store and retrieve processed articles, reducing processing time for repeated requests.

### Features
- **Automatic Caching**: All processed articles are cached automatically
- **TTL Support**: Cache expiration (default: 24 hours)
- **Access Tracking**: Tracks access count and last accessed time
- **Search**: Find articles by category
- **Statistics**: View processing statistics
- **Cleanup**: Remove old cached articles

### Usage

```python
# Process with caching (default)
processor = ArticleProcessor(use_cache=True)
result = processor.process_url("https://example.com/article")

# Process without caching
processor_no_cache = ArticleProcessor(use_cache=False)

# Force refresh (bypass cache)
result = processor.process_url("https://example.com/article", force_refresh=True)

# Get cached articles
cached = processor.get_cached_articles(category="technology", limit=10)

# Get statistics
stats = processor.get_statistics()
print(f"Total articles: {stats['total_articles']}")
print(f"Categories: {stats['category_distribution']}")

# Cleanup old articles (older than 30 days)
deleted = processor.cleanup_old_cache(days=30)
print(f"Deleted {deleted} old articles")
```

### Database Schema
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    url_hash TEXT UNIQUE,
    title TEXT,
    text TEXT,
    classification TEXT,
    summary TEXT,
    sentiment_analysis TEXT,
    keyword_analysis TEXT,
    metadata_analysis TEXT,
    processed_at TEXT,
    access_count INTEGER,
    last_accessed TEXT
)
```

---

## Export Functionality

### Overview
Export processed articles to various formats for reporting and archival.

### Supported Formats
1. **JSON** - Complete data export
2. **CSV** - Tabular format for spreadsheets
3. **Markdown** - Human-readable documentation
4. **HTML** - Styled web page

### Usage

```python
result = processor.process_url("https://example.com/article")

# Export to JSON
json_path = processor.export_article(result, format="json")

# Export to Markdown
md_path = processor.export_article(result, format="markdown")

# Export to HTML
html_path = processor.export_article(result, format="html")

# Export multiple articles to CSV
articles = processor.process_urls(["url1", "url2", "url3"])
csv_path = processor.exporter.export_to_csv(articles)

print(f"Exported to: {json_path}")
```

### File Naming
Files are automatically named with:
- Title slug (sanitized)
- Timestamp
- Appropriate extension

Example: `elon-musk-announces-new-ai-project_20260127_143022.json`

### Export Locations
Default: `exports/` directory (created automatically)

---

## API Enhancements

### New Endpoints

#### 1. Export Article
```bash
POST /api/export
```

Export a processed article to a file.

**Request Body:**
```json
{
  "url": "https://example.com/article",
  "format": "json"
}
```

**Response:**
```json
{
  "message": "Article exported successfully",
  "filepath": "exports/article_20260127_143022.json",
  "format": "json"
}
```

#### 2. Get Cached Articles
```bash
GET /api/cached?category=technology&limit=10
```

Retrieve cached articles from the database.

**Query Parameters:**
- `category` (optional): Filter by category
- `limit` (optional): Number of results (default: 10, max: 50)

**Response:**
```json
{
  "count": 10,
  "articles": [...]
}
```

#### 3. Get Statistics
```bash
GET /api/statistics
```

Get processing statistics.

**Response:**
```json
{
  "total_articles": 150,
  "category_distribution": {
    "technology": 45,
    "politics": 30,
    "business": 25
  },
  "top_articles": [...]
}
```

### Updated Response Format

The `/api/process` endpoint now returns enhanced data:

```json
{
  "title": "Article Title",
  "text": "Full article text...",
  "summary": "Article summary...",
  "classification": {
    "top_label": "technology",
    "top_score": 0.95
  },
  "sentiment_analysis": {
    "sentiment": {"label": "POSITIVE", "score": 0.85},
    "emotions": [...]
  },
  "keyword_analysis": {
    "keywords": [...],
    "entities": [...],
    "key_phrases": [...]
  },
  "metadata_analysis": {
    "reading_time": {...},
    "quality_score": {...},
    "readability": {...},
    "text_statistics": {...}
  }
}
```

---

## Telegram Bot Enhancements

### New Commands

#### `/stats`
View processing statistics
```
/stats

Response:
📊 Statistics

Total Articles: 150

Category Distribution:
• technology: 45
• politics: 30
• business: 25
```

#### `/cached`
View recently cached articles
```
/cached

Response:
📚 Recent Cached Articles

1. Elon Musk Announces New AI Project
   Category: technology

2. Climate Summit Reaches Agreement
   Category: environment
```

### Enhanced Article Analysis

When you send a URL, the bot now shows:

```
📰 Article Analysis

Title: Article Title

Category: TECHNOLOGY
Confidence: 95.0%

😊 Sentiment: POSITIVE (85.0%)
Emotions: joy, optimism, trust

⏱️ Reading Time: 5 minutes read
📊 Word Count: 1000
⭐ Quality: 87/100 (Very Good)

🔑 Keywords: artificial, intelligence, technology, innovation
🏷️ Entities: Elon Musk (PER), Tesla (ORG)

Summary:
[Article summary here...]

Source: https://example.com/article
```

### Commands Summary
- `/start` - Welcome message and feature overview
- `/help` - Help information
- `/stats` - View statistics
- `/cached` - View recent cached articles
- Send URL - Process and analyze article

---

## Performance Considerations

### Caching Benefits
- **Reduces processing time** by ~90% for cached articles
- **Saves API costs** for transformer models
- **Improves user experience** with instant responses

### Resource Usage
New features add minimal overhead:
- Sentiment analysis: ~1-2 seconds
- Keyword extraction: ~0.5-1 seconds
- Metadata analysis: ~0.1 seconds
- Total additional time: ~2-4 seconds per article

### Optimization Tips
1. **Enable caching** for production use
2. **Use batch processing** for multiple articles
3. **Set appropriate cache TTL** based on your needs
4. **Clean old cache** regularly to save disk space

---

## Configuration

All features are configurable via environment variables:

```env
# Cache settings
USE_CACHE=true
CACHE_TTL_HOURS=24

# Export settings
EXPORT_DIR=exports

# Advanced features
USE_ADVANCED_FEATURES=true

# Database
DATABASE_PATH=articles.db
```

---

## Examples

### Complete Example

```python
from src.main import ArticleProcessor

# Initialize processor with all features
processor = ArticleProcessor(
    use_cache=True,
    use_advanced_features=True
)

# Process an article
url = "https://www.bbc.com/news/technology-article"
result = processor.process_url(url)

# Print comprehensive analysis
print(f"Title: {result['title']}")
print(f"Category: {result['classification']['top_label']}")
print(f"Sentiment: {result['sentiment_analysis']['sentiment']['label']}")
print(f"Reading Time: {result['metadata_analysis']['reading_time']['formatted']}")
print(f"Quality Score: {result['metadata_analysis']['quality_score']['score']}/100")

# Export to multiple formats
processor.export_article(result, format="json")
processor.export_article(result, format="markdown")
processor.export_article(result, format="html")

# View statistics
stats = processor.get_statistics()
print(f"Total processed articles: {stats['total_articles']}")
```

---

## Support

For issues or questions about new features:
1. Check this documentation
2. Review the code in respective modules
3. Open an issue on GitHub
4. Contact the development team

---

**Happy Analyzing! 🎉**
