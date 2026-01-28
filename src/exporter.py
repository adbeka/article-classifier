"""
Export functionality for articles in various formats (JSON, CSV, Markdown, HTML).
"""
import json
import csv
from typing import Dict, List
from datetime import datetime
from pathlib import Path


class ArticleExporter:
    """Exporter for saving articles in different formats."""
    
    def __init__(self, output_dir: str = "exports"):
        """
        Initialize the exporter.
        
        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_to_json(self, article: Dict[str, any], filename: str = None) -> str:
        """
        Export article to JSON format.
        
        Args:
            article: Article dictionary
            filename: Optional custom filename
            
        Returns:
            Path to the exported file
        """
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            title_slug = self._slugify(article.get('title', 'article'))
            filename = f"{title_slug}_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_multiple_to_json(self, articles: List[Dict[str, any]], filename: str = None) -> str:
        """
        Export multiple articles to a single JSON file.
        
        Args:
            articles: List of article dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to the exported file
        """
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"articles_export_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        export_data = {
            'export_date': datetime.utcnow().isoformat(),
            'article_count': len(articles),
            'articles': articles
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_to_csv(self, articles: List[Dict[str, any]], filename: str = None) -> str:
        """
        Export articles to CSV format.
        
        Args:
            articles: List of article dictionaries
            filename: Optional custom filename
            
        Returns:
            Path to the exported file
        """
        if not articles:
            raise ValueError("No articles to export")
        
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"articles_export_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Define CSV columns
        fieldnames = [
            'url',
            'title',
            'category',
            'confidence',
            'sentiment',
            'sentiment_score',
            'reading_time_minutes',
            'word_count',
            'quality_score',
            'publish_date',
            'summary'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for article in articles:
                row = {
                    'url': article.get('url', ''),
                    'title': article.get('title', ''),
                    'category': article.get('classification', {}).get('top_label', ''),
                    'confidence': article.get('classification', {}).get('top_score', ''),
                    'sentiment': article.get('sentiment_analysis', {}).get('sentiment', {}).get('label', ''),
                    'sentiment_score': article.get('sentiment_analysis', {}).get('sentiment', {}).get('score', ''),
                    'reading_time_minutes': article.get('metadata_analysis', {}).get('reading_time', {}).get('minutes', ''),
                    'word_count': article.get('metadata_analysis', {}).get('text_statistics', {}).get('word_count', ''),
                    'quality_score': article.get('metadata_analysis', {}).get('quality_score', {}).get('score', ''),
                    'publish_date': article.get('publish_date', ''),
                    'summary': article.get('summary', '')
                }
                writer.writerow(row)
        
        return str(filepath)
    
    def export_to_markdown(self, article: Dict[str, any], filename: str = None) -> str:
        """
        Export article to Markdown format.
        
        Args:
            article: Article dictionary
            filename: Optional custom filename
            
        Returns:
            Path to the exported file
        """
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            title_slug = self._slugify(article.get('title', 'article'))
            filename = f"{title_slug}_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        # Build markdown content
        md_content = []
        
        # Title
        title = article.get('title', 'Untitled')
        md_content.append(f"# {title}\n")
        
        # Metadata
        md_content.append("## Metadata\n")
        md_content.append(f"- **URL**: {article.get('url', 'N/A')}")
        
        if article.get('publish_date'):
            md_content.append(f"- **Published**: {article.get('publish_date')}")
        
        if article.get('authors'):
            authors = ', '.join(article.get('authors', []))
            md_content.append(f"- **Authors**: {authors}")
        
        # Classification
        classification = article.get('classification', {})
        if classification:
            md_content.append(f"\n## Classification\n")
            md_content.append(f"- **Category**: {classification.get('top_label', 'N/A')}")
            md_content.append(f"- **Confidence**: {classification.get('top_score', 0) * 100:.1f}%")
        
        # Sentiment Analysis
        sentiment_analysis = article.get('sentiment_analysis', {})
        if sentiment_analysis:
            sentiment = sentiment_analysis.get('sentiment', {})
            md_content.append(f"\n## Sentiment Analysis\n")
            md_content.append(f"- **Sentiment**: {sentiment.get('label', 'N/A')}")
            md_content.append(f"- **Score**: {sentiment.get('score', 0) * 100:.1f}%")
            
            emotions = sentiment_analysis.get('emotions', [])
            if emotions:
                md_content.append(f"\n### Top Emotions\n")
                for emotion in emotions[:3]:
                    md_content.append(f"- {emotion['label']}: {emotion['score'] * 100:.1f}%")
        
        # Metadata Analysis
        metadata_analysis = article.get('metadata_analysis', {})
        if metadata_analysis:
            md_content.append(f"\n## Reading Information\n")
            
            reading_time = metadata_analysis.get('reading_time', {})
            if reading_time:
                md_content.append(f"- **Reading Time**: {reading_time.get('formatted', 'N/A')}")
            
            quality_score = metadata_analysis.get('quality_score', {})
            if quality_score:
                md_content.append(f"- **Quality Score**: {quality_score.get('score', 0)}/100 ({quality_score.get('grade', 'N/A')})")
            
            readability = metadata_analysis.get('readability', {})
            if readability:
                md_content.append(f"- **Readability**: {readability.get('interpretation', 'N/A')} ({readability.get('grade_level', 'N/A')})")
        
        # Keywords
        keyword_analysis = article.get('keyword_analysis', {})
        if keyword_analysis:
            keywords = keyword_analysis.get('keywords', [])
            if keywords:
                md_content.append(f"\n## Top Keywords\n")
                keyword_list = [f"{kw['word']} ({kw['frequency']})" for kw in keywords[:10]]
                md_content.append(', '.join(keyword_list))
            
            entities = keyword_analysis.get('entities', [])
            if entities:
                md_content.append(f"\n## Named Entities\n")
                for entity in entities[:10]:
                    md_content.append(f"- **{entity['text']}** ({entity['type']})")
        
        # Summary
        summary = article.get('summary', '')
        if summary:
            md_content.append(f"\n## Summary\n")
            md_content.append(summary)
        
        # Full Text
        text = article.get('text', '')
        if text:
            md_content.append(f"\n## Full Article\n")
            md_content.append(text)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        return str(filepath)
    
    def export_to_html(self, article: Dict[str, any], filename: str = None) -> str:
        """
        Export article to HTML format.
        
        Args:
            article: Article dictionary
            filename: Optional custom filename
            
        Returns:
            Path to the exported file
        """
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            title_slug = self._slugify(article.get('title', 'article'))
            filename = f"{title_slug}_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        # Build HTML content
        title = article.get('title', 'Untitled')
        classification = article.get('classification', {})
        sentiment_analysis = article.get('sentiment_analysis', {})
        metadata_analysis = article.get('metadata_analysis', {})
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2980b9;
            margin-top: 30px;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-weight: bold;
            margin-right: 10px;
        }}
        .category {{
            background-color: #3498db;
            color: white;
        }}
        .sentiment-positive {{
            background-color: #2ecc71;
            color: white;
        }}
        .sentiment-negative {{
            background-color: #e74c3c;
            color: white;
        }}
        .sentiment-neutral {{
            background-color: #95a5a6;
            color: white;
        }}
        .summary {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
        .article-text {{
            text-align: justify;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    
    <div class="metadata">
        <p><strong>URL:</strong> <a href="{article.get('url', '')}">{article.get('url', 'N/A')}</a></p>
        <p>
            <span class="badge category">{classification.get('top_label', 'N/A').upper()}</span>
"""
        
        # Add sentiment badge
        sentiment = sentiment_analysis.get('sentiment', {})
        sentiment_label = sentiment.get('label', 'NEUTRAL')
        sentiment_class = f"sentiment-{sentiment_label.lower()}"
        html_content += f'            <span class="badge {sentiment_class}">{sentiment_label}</span>\n'
        
        # Add reading time
        reading_time = metadata_analysis.get('reading_time', {})
        if reading_time:
            html_content += f'            <span>{reading_time.get("formatted", "")}</span>\n'
        
        html_content += "        </p>\n    </div>\n"
        
        # Summary
        summary = article.get('summary', '')
        if summary:
            html_content += f'''
    <div class="summary">
        <h2>Summary</h2>
        <p>{summary}</p>
    </div>
'''
        
        # Full text
        text = article.get('text', '')
        if text:
            html_content += f'''
    <h2>Full Article</h2>
    <div class="article-text">
        <p>{text.replace(chr(10), '</p><p>')}</p>
    </div>
'''
        
        html_content += """
</body>
</html>
"""
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _slugify(self, text: str, max_length: int = 50) -> str:
        """
        Convert text to a filename-safe slug.
        
        Args:
            text: Text to slugify
            max_length: Maximum length of slug
            
        Returns:
            Slugified text
        """
        import re
        
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Truncate to max length
        if len(slug) > max_length:
            slug = slug[:max_length].rsplit('-', 1)[0]
        
        return slug or 'article'
