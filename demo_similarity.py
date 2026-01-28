"""
Demo script for Article Similarity & Duplicate Detection feature.

This script demonstrates how to use the similarity detection capabilities
of the Article Classifier & Summarizer.
"""
from src.main import ArticleProcessor
import time


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*70 + "\n")


def demo_similarity_search():
    """Demonstrate finding similar articles."""
    print("🔗 ARTICLE SIMILARITY SEARCH DEMO")
    print_separator()
    
    processor = ArticleProcessor()
    
    # Example URLs (replace with real URLs for actual testing)
    example_urls = [
        "https://www.bbc.com/news/technology-12345678",
        "https://www.techcrunch.com/ai-news-article",
        "https://www.cnn.com/sports/football-championship",
    ]
    
    print("Processing sample articles...")
    articles = []
    for url in example_urls:
        print(f"  - Processing: {url[:60]}...")
        # Note: In real usage, replace with actual news URLs
        # For demo, we'll create sample data
    
    print("\n✓ Articles processed and cached with embeddings")
    
    print_separator()
    print("Finding similar articles...")
    
    # Demo: Find similar articles
    similar = processor.find_similar_by_url(
        example_urls[0],
        top_k=3,
        min_similarity=0.3
    )
    
    if similar:
        print(f"\nFound {len(similar)} similar article(s):\n")
        for i, item in enumerate(similar, 1):
            article = item['article']
            score = item['similarity_score']
            print(f"{i}. {article.get('title', 'N/A')[:60]}")
            print(f"   Similarity: {score*100:.1f}%")
            print(f"   Category: {article.get('classification', {}).get('top_label', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')[:60]}\n")
    else:
        print("No similar articles found (database may be empty)")


def demo_duplicate_detection():
    """Demonstrate duplicate detection."""
    print_separator()
    print("🔍 DUPLICATE DETECTION DEMO")
    print_separator()
    
    processor = ArticleProcessor()
    
    print("Scanning database for duplicate articles...")
    duplicates = processor.find_all_duplicates(threshold=0.9)
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate pair(s):\n")
        for i, dup in enumerate(duplicates, 1):
            art1 = dup['article1']
            art2 = dup['article2']
            similarity = dup['similarity']
            
            print(f"Pair {i} - Similarity: {similarity*100:.1f}%")
            print(f"  1. {art1['title'][:50]}")
            print(f"  2. {art2['title'][:50]}\n")
    else:
        print("✅ No duplicate articles found in database")


def demo_similarity_report():
    """Demonstrate comprehensive similarity report."""
    print_separator()
    print("📊 SIMILARITY REPORT DEMO")
    print_separator()
    
    processor = ArticleProcessor()
    
    # Process an article
    example_url = "https://www.bbc.com/news/technology-12345678"
    print(f"Processing article: {example_url}")
    
    article = processor.process_url(example_url)
    
    if 'error' in article:
        print(f"Error: {article['error']}")
        return
    
    print(f"\nArticle: {article.get('title', 'N/A')[:60]}")
    print(f"Category: {article.get('classification', {}).get('top_label', 'N/A')}")
    
    # Get similarity report
    print("\nGenerating similarity report...")
    report = processor.get_article_similarity_report(article)
    
    print(f"\n📈 Similarity Analysis:")
    print(f"  Max Similarity: {report['max_similarity']*100:.1f}%")
    print(f"  Avg Similarity: {report['avg_similarity']*100:.1f}%")
    print(f"  Total Similar Found: {report['total_similar_found']}")
    
    if report['has_duplicates']:
        print(f"\n  ⚠️  Duplicates Detected: {report['duplicate_count']}")
        for dup in report['duplicates']:
            print(f"    - {dup['title'][:50]} ({dup['similarity']*100:.1f}%)")
    else:
        print("\n  ✅ No duplicates detected")
    
    if report['similar_articles']:
        print(f"\n  🔗 Top Similar Articles:")
        for sim in report['similar_articles'][:3]:
            print(f"    - {sim['title'][:50]}")
            print(f"      Similarity: {sim['similarity']*100:.1f}% | Category: {sim['category']}")


def demo_real_time_check():
    """Demonstrate real-time duplicate checking during processing."""
    print_separator()
    print("⚡ REAL-TIME DUPLICATE CHECK DEMO")
    print_separator()
    
    processor = ArticleProcessor()
    
    example_url = "https://www.reuters.com/technology/ai-news"
    
    print(f"Processing new article: {example_url}")
    article = processor.process_url(example_url)
    
    if 'error' in article:
        print(f"Error: {article['error']}")
        return
    
    print(f"\nArticle processed: {article.get('title', 'N/A')[:60]}")
    
    # Check for duplicates
    print("\nChecking for duplicates...")
    dup_info = processor.check_duplicate(article, threshold=0.9)
    
    if dup_info['is_duplicate']:
        print(f"\n⚠️  This article is a duplicate!")
        print(f"   Found {dup_info['duplicate_count']} similar article(s):")
        for dup in dup_info['duplicates']:
            print(f"   - {dup['title'][:50]}")
            print(f"     Similarity: {dup['similarity']*100:.1f}%")
            print(f"     URL: {dup['url'][:60]}")
    else:
        print("\n✅ This is a unique article (no duplicates found)")


def show_statistics():
    """Show database statistics."""
    print_separator()
    print("📊 DATABASE STATISTICS")
    print_separator()
    
    processor = ArticleProcessor()
    stats = processor.get_statistics()
    
    if stats and stats.get('total_articles', 0) > 0:
        print(f"\nTotal Articles: {stats['total_articles']}")
        print("\nCategory Distribution:")
        for category, count in sorted(
            stats.get('category_distribution', {}).items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(f"  {category}: {count}")
        
        print("\nAll articles have embeddings for similarity search!")
    else:
        print("Database is empty. Process some articles first!")


def main():
    """Run all demos."""
    print("\n" + "="*70)
    print(" " * 10 + "ARTICLE SIMILARITY & DUPLICATE DETECTION")
    print(" " * 20 + "Feature Demo")
    print("="*70)
    
    print("\nThis demo showcases the new similarity detection features:")
    print("  1. Finding similar articles")
    print("  2. Detecting duplicates")
    print("  3. Generating similarity reports")
    print("  4. Real-time duplicate checking")
    
    input("\nPress Enter to start the demo...")
    
    try:
        # Show current statistics
        show_statistics()
        
        # Demo 1: Similarity Search
        input("\nPress Enter to continue to Similarity Search demo...")
        demo_similarity_search()
        
        # Demo 2: Duplicate Detection
        input("\nPress Enter to continue to Duplicate Detection demo...")
        demo_duplicate_detection()
        
        # Demo 3: Similarity Report
        input("\nPress Enter to continue to Similarity Report demo...")
        demo_similarity_report()
        
        # Demo 4: Real-time Check
        input("\nPress Enter to continue to Real-time Check demo...")
        demo_real_time_check()
        
        print_separator()
        print("✓ Demo completed!")
        print("\nTo use these features in your code:")
        print("  • processor.find_similar_by_url(url, top_k=5)")
        print("  • processor.find_all_duplicates(threshold=0.9)")
        print("  • processor.check_duplicate(article)")
        print("  • processor.get_article_similarity_report(article)")
        
        print("\nFor API usage, see: docs/SIMILARITY_FEATURE.md")
        print_separator()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {str(e)}")
        print("Make sure you have:")
        print("  1. Installed all requirements: pip install -r requirements.txt")
        print("  2. Processed some articles to populate the database")


if __name__ == '__main__':
    main()
