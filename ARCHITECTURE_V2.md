# Enhanced System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Input Sources                                │
├──────────────┬──────────────┬──────────────┬───────────────────────┤
│   Web URLs   │  Chrome Ext  │ Telegram Bot │   API Requests        │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬──────────────┘
       │              │              │                │
       └──────────────┴──────────────┴────────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │   ArticleProcessor      │
                  │     (main.py)           │
                  │   [Enhanced v2.0]       │
                  └───────────┬─────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  Cache Check      │
                    │  (database.py)    │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │ Cached? ──Yes──► Return
                    │         │
                    │         No
                    │         ▼
                    └─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
  ┌──────────┐        ┌──────────┐        ┌──────────┐
  │ Scraper  │        │Classifier│        │Summarizer│
  │ (Step 1) │        │ (Step 2) │        │ (Step 3) │
  └────┬─────┘        └────┬─────┘        └────┬─────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │   [NEW] Advanced Analysis   │
            │                             │
   ┌────────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐
   │   Sentiment     │  │   Keyword       │  │   Metadata      │
   │   Analyzer      │  │   Extractor     │  │   Analyzer      │
   │   (Step 4)      │  │   (Step 5)      │  │   (Step 6)      │
   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │   Enhanced Result       │
                    │  - Title                │
                    │  - Text                 │
                    │  - Category             │
                    │  - Summary              │
                    │  - Sentiment ★NEW       │
                    │  - Keywords ★NEW        │
                    │  - Entities ★NEW        │
                    │  - Reading Time ★NEW    │
                    │  - Quality Score ★NEW   │
                    └──────────┬──────────────┘
                               │
                  ┌────────────┴────────────┐
                  │   Save to Cache         │
                  │   (database.py)         │
                  └────────────┬────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
   ┌─────────┐          ┌──────────┐          ┌──────────┐
   │ Export  │          │ Flask    │          │ Telegram │
   │ JSON/CSV│          │ API      │          │   Bot    │
   │ MD/HTML │          │          │          │          │
   └─────────┘          └──────────┘          └──────────┘
```

## Component Details (Enhanced)

### 1. Article Scraper (src/scraper.py)
**Status**: Unchanged
- Extracts article content from URLs
- Uses newspaper3k library
- Returns: title, text, authors, date, image

### 2. Article Classifier (src/classifier.py)
**Status**: Unchanged
- Zero-shot classification with BART
- 10+ category support
- Confidence scores

### 3. Article Summarizer (src/summarizer.py)
**Status**: Unchanged
- Text summarization with BART
- Configurable length
- Chunk processing for long articles

### 4. Sentiment Analyzer (src/sentiment_analyzer.py) ★NEW
**Features**:
- Sentiment detection (POSITIVE/NEGATIVE/NEUTRAL)
- Emotion analysis (joy, sadness, anger, fear, surprise, etc.)
- Confidence scores
- Emoji mapping

**Models Used**:
- DistilBERT for sentiment
- RoBERTa for emotions

### 5. Keyword Extractor (src/keyword_extractor.py) ★NEW
**Features**:
- Frequency-based keyword extraction
- Key phrase detection (n-grams)
- Named Entity Recognition (NER)
- Entity types: PER, ORG, LOC, MISC
- Stopword filtering

**Models Used**:
- BERT-base-NER

### 6. Metadata Analyzer (src/metadata_analyzer.py) ★NEW
**Features**:
- Reading time estimation (words/minute)
- Quality score calculation (0-100)
- Flesch Reading Ease (readability)
- Grade level assessment
- Text statistics (words, sentences, paragraphs)

**Algorithms**:
- Flesch Reading Ease formula
- Custom quality scoring system
- Syllable counting

### 7. Database (src/database.py) ★NEW
**Features**:
- SQLite-based article storage
- TTL-based caching (configurable)
- URL hashing for fast lookups
- Access tracking
- Category search
- Statistics generation
- Auto-cleanup

**Schema**:
```sql
articles (
    id, url, url_hash, title, text,
    classification, summary,
    sentiment_analysis,
    keyword_analysis,
    metadata_analysis,
    processed_at, access_count, last_accessed
)
```

### 8. Exporter (src/exporter.py) ★NEW
**Formats**:
- JSON (complete data)
- CSV (tabular)
- Markdown (human-readable)
- HTML (styled webpage)

**Features**:
- Auto filename generation
- Timestamp inclusion
- Title slugification
- Custom output directory

### 9. Enhanced API (src/api.py)
**New Endpoints**:
- `POST /api/export` - Export articles
- `GET /api/cached` - Get cached articles
- `GET /api/statistics` - Processing stats

**Enhanced Responses**:
- All endpoints return full analysis
- Includes sentiment, keywords, metadata

### 10. Enhanced Telegram Bot (src/telegram_bot.py)
**New Commands**:
- `/stats` - View statistics
- `/cached` - Browse cached articles

**Enhanced Output**:
- Sentiment with emojis
- Reading time and quality
- Keywords and entities
- Emotion analysis

## Data Flow

### Processing Pipeline
```
URL → Scraper → Classifier → Summarizer
                    ↓
              Sentiment Analyzer
                    ↓
              Keyword Extractor
                    ↓
              Metadata Analyzer
                    ↓
                 Database
                    ↓
          Return / Export / Display
```

### Caching Flow
```
Request → Check Cache
            │
      ┌─────┴─────┐
      │           │
   Found      Not Found
      │           │
   Return    Process → Cache → Return
```

## Technology Stack

### Core Libraries
- **Transformers** (Hugging Face) - NLP models
- **Torch** - Deep learning backend
- **newspaper3k** - Web scraping
- **Flask** - API server
- **python-telegram-bot** - Bot interface
- **SQLite3** - Database (built-in)

### Models Used
1. **BART-large-mnli** - Classification
2. **BART-large-cnn** - Summarization
3. **DistilBERT-SST-2** - Sentiment
4. **RoBERTa-emotion** - Emotions
5. **BERT-base-NER** - Named entities

## Performance Metrics

### Processing Times (approximate)
- Scraping: ~2 seconds
- Classification: ~3 seconds
- Summarization: ~3 seconds
- Sentiment: ~1 second ★NEW
- Keywords: ~1 second ★NEW
- Metadata: ~0.1 seconds ★NEW
- **Total**: ~10 seconds (first time)
- **Cached**: ~0.1 seconds (90% improvement!)

### Resource Usage
- Memory: ~2-4 GB (models loaded)
- Disk: ~5 GB (models) + database
- CPU: Moderate during processing
- GPU: Optional but recommended

## Scalability

### Horizontal Scaling
- API can be load-balanced
- Database can be upgraded to PostgreSQL
- Cache can use Redis
- Models can be served separately

### Optimization Tips
1. Use GPU for faster inference
2. Enable caching for frequent articles
3. Batch process multiple articles
4. Use CDN for model downloads
5. Implement rate limiting

## Security Considerations

### Input Validation
- URL format checking
- SQL injection prevention (parameterized queries)
- Request size limits
- Rate limiting on API

### Data Privacy
- No personal data stored
- URL hashing for privacy
- Optional encryption for sensitive data
- Configurable data retention

## Monitoring & Analytics

### Available Metrics
- Total articles processed
- Category distribution
- Most accessed articles
- Processing times
- Cache hit rates
- Error rates

### Statistics Endpoint
```json
{
  "total_articles": 1500,
  "category_distribution": {
    "technology": 450,
    "politics": 300,
    "business": 250
  },
  "cache_hit_rate": 0.85,
  "average_processing_time": 9.5
}
```

## Future Architecture Improvements

### Potential Enhancements
1. **Microservices** - Separate services for each feature
2. **Message Queue** - RabbitMQ/Kafka for async processing
3. **Containerization** - Docker for easy deployment
4. **Kubernetes** - Orchestration for scaling
5. **GraphQL API** - Alternative to REST
6. **Real-time Updates** - WebSocket support
7. **Distributed Cache** - Redis cluster
8. **Analytics Dashboard** - Real-time monitoring

---

## Version History

### v2.0 (Current)
- ✅ Sentiment analysis
- ✅ Keyword extraction
- ✅ Metadata analysis
- ✅ Database caching
- ✅ Export functionality
- ✅ Enhanced API
- ✅ Enhanced bot

### v1.0
- Basic scraping
- Classification
- Summarization
- Simple API
- Basic bot

---

**Architecture designed for scalability, performance, and extensibility.**
