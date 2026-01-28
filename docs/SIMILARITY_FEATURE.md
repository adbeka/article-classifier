# Article Similarity & Duplicate Detection Feature 🔗

## Overview

The **Article Similarity & Duplicate Detection** feature uses advanced semantic embeddings to find related articles, detect duplicates, and recommend similar content. This powerful addition enables content discovery, prevents redundant processing, and helps identify related news stories.

## Features

### 1. **Semantic Similarity Search**
- Find articles with similar content using AI-powered embeddings
- Uses sentence-transformers for high-quality semantic understanding
- Adjustable similarity thresholds
- Returns ranked results by relevance

### 2. **Duplicate Detection**
- Automatically identify duplicate or near-duplicate articles
- Configurable similarity threshold (default: 90%)
- Batch duplicate scanning across entire database
- Prevents redundant processing and storage

### 3. **Content-Based Recommendations**
- Recommend related articles based on content similarity
- Find alternative perspectives on the same topic
- Discover related news stories automatically

### 4. **Article Clustering**
- Group similar articles into topic clusters
- Identify trending themes across multiple articles
- Organize large article collections

## How It Works

### Technical Architecture

The similarity system uses **sentence-transformers** (specifically the `all-MiniLM-L6-v2` model) to generate 384-dimensional embedding vectors for each article. These embeddings capture the semantic meaning of the article content.

**Key Steps:**
1. **Embedding Generation**: Article title and summary/content are combined and converted to a vector
2. **Similarity Calculation**: Cosine similarity is computed between embedding vectors
3. **Ranking**: Articles are ranked by similarity score (0-1, where 1 is identical)
4. **Storage**: Embeddings are stored in the database as BLOB for fast retrieval

### Why Sentence-Transformers?

- **Fast**: Generates embeddings in milliseconds
- **Accurate**: State-of-the-art semantic understanding
- **Efficient**: Small model size (80MB) with excellent performance
- **Multilingual**: Supports multiple languages

## Usage

### Python API

#### 1. Find Similar Articles by URL

```python
from src.main import ArticleProcessor

processor = ArticleProcessor()

# Find similar articles
similar = processor.find_similar_by_url(
    url="https://example.com/article",
    top_k=5,
    min_similarity=0.5
)

# Display results
for item in similar:
    article = item['article']
    score = item['similarity_score']
    print(f"Title: {article['title']}")
    print(f"Similarity: {score * 100:.1f}%")
    print(f"URL: {article['url']}\n")
```

#### 2. Check for Duplicates

```python
# Check if article is a duplicate
article = processor.process_url("https://example.com/article")
duplicate_info = processor.check_duplicate(article, threshold=0.9)

if duplicate_info['is_duplicate']:
    print(f"⚠️ Found {duplicate_info['duplicate_count']} duplicate(s):")
    for dup in duplicate_info['duplicates']:
        print(f"  - {dup['title']} ({dup['similarity']*100:.1f}%)")
else:
    print("✅ No duplicates found")
```

#### 3. Find All Duplicates in Database

```python
# Scan entire database for duplicates
duplicates = processor.find_all_duplicates(threshold=0.9)

print(f"Found {len(duplicates)} duplicate pairs:")
for dup in duplicates:
    print(f"\nSimilarity: {dup['similarity']*100:.1f}%")
    print(f"  1. {dup['article1']['title']}")
    print(f"  2. {dup['article2']['title']}")
```

#### 4. Get Comprehensive Similarity Report

```python
# Get full similarity analysis
article = processor.process_url("https://example.com/article")
report = processor.get_article_similarity_report(article)

print(f"Has duplicates: {report['has_duplicates']}")
print(f"Max similarity: {report['max_similarity']*100:.1f}%")
print(f"Avg similarity: {report['avg_similarity']*100:.1f}%")
print(f"\nTop 5 similar articles:")
for sim in report['similar_articles']:
    print(f"  - {sim['title']} ({sim['similarity']*100:.1f}%)")
```

### REST API

#### Find Similar Articles

```bash
curl -X POST http://localhost:5000/api/similar \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "top_k": 5,
    "min_similarity": 0.5
  }'
```

**Response:**
```json
{
  "query_article": {
    "title": "AI Revolutionizes Healthcare",
    "url": "https://example.com/article",
    "category": "Technology"
  },
  "similar_count": 3,
  "similar_articles": [
    {
      "title": "Machine Learning in Medical Diagnosis",
      "url": "https://example.com/ml-diagnosis",
      "category": "Technology",
      "similarity_score": 0.85,
      "summary": "..."
    }
  ]
}
```

#### Find Duplicates

```bash
curl http://localhost:5000/api/duplicates?threshold=0.9
```

**Response:**
```json
{
  "count": 2,
  "duplicates": [
    {
      "article1": {
        "title": "Article Title",
        "url": "https://example.com/article1"
      },
      "article2": {
        "title": "Similar Article Title",
        "url": "https://example.com/article2"
      },
      "similarity": 0.92
    }
  ]
}
```

#### Get Similarity Report

```bash
curl -X POST http://localhost:5000/api/similarity-report \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

### Telegram Bot

#### Find Similar Articles

```
/similar https://example.com/article
```

The bot will respond with:
```
🔗 Similar Articles

Query: AI Revolutionizes Healthcare

Found 3 similar article(s):

1. Machine Learning in Medical Diagnosis
   Category: Technology
   Similarity: 85.3%
   URL: https://example.com/ml-diagnosis

2. Healthcare AI Applications
   Category: Science
   Similarity: 78.2%
   URL: https://example.com/healthcare-ai
```

#### Find All Duplicates

```
/duplicates
```

The bot will scan the database and report any duplicate pairs found.

## Configuration

### Similarity Thresholds

- **High Similarity** (0.8 - 1.0): Articles about the same specific topic
- **Medium Similarity** (0.5 - 0.8): Related topics or themes
- **Low Similarity** (0.3 - 0.5): Loosely related content
- **Duplicate** (0.9+): Likely the same article from different sources

### Performance Considerations

**Database Size:**
- Small (<1000 articles): Instant results
- Medium (1000-10000): Sub-second results
- Large (10000+): Consider using vector databases like FAISS or Milvus

**Optimization Tips:**
1. Cache embeddings in database (already implemented)
2. Limit search to recent articles for faster results
3. Use batch processing for large-scale duplicate detection
4. Consider implementing approximate nearest neighbor search for very large databases

## Advanced Usage

### Custom Similarity Model

```python
from src.similarity_analyzer import SimilarityAnalyzer

# Use a different model
analyzer = SimilarityAnalyzer(model_name="paraphrase-MiniLM-L6-v2")

# Generate embedding
embedding = analyzer.generate_embedding("Your text here")
```

### Batch Similarity Analysis

```python
# Process multiple articles and find all similar pairs
articles = [article1, article2, article3, ...]

# Generate embeddings for all
for article in articles:
    article['embedding'] = analyzer.generate_article_embedding(article)

# Find all similar pairs
duplicates = analyzer.find_duplicates_in_batch(articles, threshold=0.8)
```

### Article Clustering

```python
# Group articles by similarity
clusters = analyzer.cluster_similar_articles(
    articles,
    similarity_threshold=0.7
)

# Process each cluster
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: {len(cluster)} articles")
    for idx in cluster:
        print(f"  - {articles[idx]['title']}")
```

## Use Cases

### 1. **News Aggregation**
Automatically group news articles about the same event from different sources.

### 2. **Content Curation**
Recommend related articles to readers based on what they're currently viewing.

### 3. **Duplicate Prevention**
Check if an article has already been processed before spending resources on analysis.

### 4. **Trend Detection**
Identify emerging topics by finding clusters of similar articles over time.

### 5. **Alternative Perspectives**
Find articles covering the same topic from different angles or news sources.

### 6. **Research**
Discover related research articles or news stories for comprehensive coverage.

## Database Schema

The similarity feature adds an `embedding` column to the articles table:

```sql
CREATE TABLE articles (
    ...
    embedding BLOB,  -- 384-dimensional vector stored as binary
    ...
);
```

Embeddings are:
- **Type**: BLOB (binary)
- **Size**: ~1.5KB per article (384 floats × 4 bytes)
- **Format**: numpy array serialized to bytes

## Performance Metrics

**Embedding Generation:**
- Time: ~50ms per article
- Model size: 80MB
- Memory: ~200MB during operation

**Similarity Search:**
- 100 articles: <10ms
- 1,000 articles: <100ms
- 10,000 articles: ~1 second
- Uses brute-force cosine similarity (acceptable for moderate datasets)

## Error Handling

The system gracefully handles:
- Empty or invalid article content
- Missing embeddings (generates on-demand)
- Database connection issues
- Model loading failures

## Future Enhancements

Potential improvements for production deployment:

1. **Vector Database Integration**: Use FAISS, Milvus, or Pinecone for large-scale similarity search
2. **Incremental Updates**: Only compute embeddings for new articles
3. **Multi-language Support**: Use multilingual models for cross-language similarity
4. **Topic-Specific Models**: Fine-tune models for specific domains (finance, sports, etc.)
5. **Similarity Caching**: Cache similarity scores for frequently compared articles
6. **Parallel Processing**: Batch embedding generation for faster processing

## Troubleshooting

### Issue: Slow similarity search

**Solution**: 
- Reduce the number of articles in the search pool
- Increase `min_similarity` threshold
- Consider implementing approximate nearest neighbor search

### Issue: Low similarity scores

**Solution**:
- Check article content quality (ensure full text is available)
- Verify embeddings are being generated correctly
- Try different similarity thresholds

### Issue: Memory errors

**Solution**:
- Process articles in batches
- Clear embeddings from memory after use
- Use a lighter model if needed

## API Reference

See [similarity_analyzer.py](../src/similarity_analyzer.py) for complete API documentation.

## Examples

Complete example scripts available in:
- [demo.py](../demo.py) - Basic usage
- [tests/test_similarity.py](../tests/test_similarity.py) - Comprehensive tests

## License

This feature is part of the Article Classifier & Summarizer project and follows the same license.
