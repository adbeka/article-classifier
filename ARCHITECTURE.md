# System Architecture

## Overview

The Article Classifier & Summarizer is a modular NLP system that processes news articles through a pipeline of scraping, classification, and summarization.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Input Sources                            │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   Web URLs   │  Chrome Ext  │ Telegram Bot │   API Requests     │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────────┘
       │              │              │                │
       └──────────────┴──────────────┴────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │   ArticleProcessor    │
                  │     (main.py)         │
                  └───────────┬───────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Scraper  │  │Classifier│  │Summarizer│
        │ (Step 1) │  │ (Step 2) │  │ (Step 3) │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                ┌────────────────────┐
                │   Processed Result │
                │  - Title           │
                │  - Text            │
                │  - Category        │
                │  - Confidence      │
                │  - Summary         │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   ┌────────┐      ┌──────────┐      ┌──────────┐
   │ Flask  │      │ Telegram │      │  Chrome  │
   │  API   │      │   Bot    │      │Extension │
   └────────┘      └──────────┘      └──────────┘
```

## Component Details

### 1. Article Scraper (`src/scraper.py`)

**Purpose**: Extract article content from URLs

**Technology**: 
- newspaper3k library
- BeautifulSoup4 for HTML parsing
- Requests for HTTP

**Process**:
1. Download HTML from URL
2. Parse and extract article structure
3. Extract metadata (title, authors, date)
4. Clean and format text content
5. Return structured article data

**Output**:
```python
{
    'title': str,
    'text': str,
    'authors': list,
    'publish_date': str,
    'url': str,
    'top_image': str
}
```

### 2. Article Classifier (`src/classifier.py`)

**Purpose**: Classify articles into topic categories

**Technology**: 
- Hugging Face Transformers
- BART model (facebook/bart-large-mnli)
- Zero-shot classification

**Process**:
1. Load pre-trained BART model
2. Tokenize article text
3. Run inference for each category
4. Calculate confidence scores
5. Rank categories by score

**Categories**:
- Politics
- Technology
- Business
- Entertainment
- Sports
- Science
- Health
- Environment
- Education
- World News

**Output**:
```python
{
    'top_label': str,
    'top_score': float,
    'all_labels': list,
    'all_scores': list
}
```

### 3. Article Summarizer (`src/summarizer.py`)

**Purpose**: Generate concise summaries

**Technology**: 
- Hugging Face Transformers
- BART-CNN model (facebook/bart-large-cnn)
- Abstractive summarization

**Process**:
1. Load pre-trained BART-CNN model
2. Split long articles into chunks
3. Generate summary for each chunk
4. Combine summaries
5. Return final summary

**Output**:
```python
{
    'summary': str  # 30-130 words
}
```

### 4. Main Processor (`src/main.py`)

**Purpose**: Orchestrate the complete pipeline

**Process**:
```python
def process_url(url):
    1. article = scraper.scrape_url(url)
    2. article = classifier.classify_article(article)
    3. article = summarizer.summarize_article(article)
    4. return article
```

### 5. Deployment Interfaces

#### A. Flask API (`src/api.py`)

**Endpoints**:
- `GET /` - API information
- `GET /api/health` - Health check
- `POST /api/process` - Process single URL
- `POST /api/batch` - Process multiple URLs

**Features**:
- CORS enabled for Chrome extension
- JSON input/output
- Error handling
- Rate limiting support

#### B. Telegram Bot (`src/telegram_bot.py`)

**Commands**:
- `/start` - Welcome message
- `/help` - Help information
- `<URL>` - Process article

**Features**:
- Async message handling
- User-friendly formatting
- Error messages
- Processing status updates

#### C. Chrome Extension

**Files**:
- `manifest.json` - Extension configuration
- `popup.html` - User interface
- `popup.js` - Extension logic
- `background.js` - Background tasks

**Features**:
- Current page analysis
- API server configuration
- Visual results display
- Error handling

## Data Flow

```
URL Input
   ↓
[Scraper] → Raw Article Data
   ↓
[Classifier] → Article + Category
   ↓
[Summarizer] → Complete Analysis
   ↓
Output (JSON)
```

## Technology Stack

### Backend
- Python 3.8+
- PyTorch (Deep Learning)
- Transformers (NLP Models)
- Flask (Web Framework)
- newspaper3k (Article Extraction)

### Telegram Bot
- python-telegram-bot
- Async/Await

### Chrome Extension
- Manifest V3
- JavaScript (ES6+)
- HTML5/CSS3

### ML Models
- BART (Classification)
- BART-CNN (Summarization)

## Performance Considerations

### Speed
- First run: ~30-60 seconds (model loading)
- Subsequent runs: ~5-10 seconds per article
- API mode: ~3-5 seconds (models pre-loaded)

### Memory
- Models: ~1.5GB RAM
- Processing: ~500MB per article
- Total recommended: 3GB+ RAM

### Disk Space
- Models: ~2GB
- Dependencies: ~1GB
- Total: ~3GB

## Scalability

### Current Implementation
- Single-threaded processing
- Synchronous API requests
- Local model inference

### Future Improvements
- Batch processing support
- Async API with queues
- GPU acceleration
- Model quantization
- Caching layer
- Load balancing

## Security Considerations

1. **Input Validation**: All URLs validated
2. **Rate Limiting**: Prevent abuse
3. **CORS**: Configured for extension only
4. **Environment Variables**: Secrets in .env
5. **Error Handling**: No sensitive data in errors

## Configuration

All configuration in `src/config.py`:
- Model selection
- API settings
- Category labels
- Summary length
- Server configuration

## Extension Points

### Adding New Categories
Edit `src/config.py`:
```python
CLASSIFICATION_LABELS = [
    "your_category",
    # ... existing categories
]
```

### Using Different Models
Set environment variables:
```bash
CLASSIFIER_MODEL=your-model
SUMMARIZER_MODEL=your-model
```

### Custom Processing
Extend `ArticleProcessor`:
```python
class CustomProcessor(ArticleProcessor):
    def process_url(self, url):
        result = super().process_url(url)
        # Add custom processing
        return result
```

## Testing Strategy

### Unit Tests
- Mock external dependencies
- Test individual components
- Fast execution

### Integration Tests
- Test component interactions
- Use real models (slower)
- End-to-end validation

### Manual Testing
- Test with real articles
- Verify accuracy
- UI/UX validation

## Monitoring & Logging

All components include logging:
```python
import logging
logger = logging.getLogger(__name__)
```

Log levels:
- INFO: Normal operations
- WARNING: Recoverable errors
- ERROR: Processing failures

## Troubleshooting

See README.md and QUICKSTART.md for common issues and solutions.
