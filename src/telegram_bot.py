"""
Telegram bot interface for article classification and summarization.
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.main import ArticleProcessor
from src.config import Config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize processor
processor = ArticleProcessor()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "Welcome to Article Classifier & Summarizer Bot! 🤖✨\n\n"
        "Send me a news article URL and I will:\n"
        "• 🔍 Scrape the article content\n"
        "• 🏷️ Classify it by topic\n"
        "• 📝 Generate a summary\n"
        "• 😊 Analyze sentiment\n"
        "• 🔑 Extract keywords\n"
        "• ⏱️ Calculate reading time\n"
        "• ⭐ Assess quality\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Show help information\n"
        "/stats - Show statistics\n"
        "/cached - View recent cached articles\n\n"
        "Just paste a URL to get started!"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_message = (
        "📰 Article Classifier & Summarizer Bot\n\n"
        "How to use:\n"
        "1. Copy a news article URL\n"
        "2. Paste it in the chat\n"
        "3. Wait for the analysis\n\n"
        "Supported topics:\n"
        "• Politics\n"
        "• Technology\n"
        "• Business\n"
        "• Entertainment\n"
        "• Sports\n"
        "• Science\n"
        "• Health\n"
        "• Environment\n"
        "• Education\n"
        "• World News\n\n"
        "Example:\n"
        "https://www.bbc.com/news/technology-12345678"
    )
    await update.message.reply_text(help_message)


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process URLs sent by users."""
    message_text = update.message.text
    
    # Check if the message contains a URL
    if not (message_text.startswith('http://') or message_text.startswith('https://')):
        await update.message.reply_text(
            "Please send a valid URL starting with http:// or https://"
        )
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text("🔄 Processing article with advanced analysis...")
    
    try:
        # Process the URL
        result = processor.process_url(message_text)
        
        if 'error' in result:
            await processing_msg.edit_text(f"❌ Error: {result['error']}")
            return
        
        # Format the response with enhanced features
        category = result['classification']['top_label']
        confidence = result['classification']['top_score']
        title = result.get('title', 'N/A')
        summary = result.get('summary', 'N/A')
        
        response = f"📰 *Article Analysis*\n\n*Title:* {title}\n\n"
        response += f"*Category:* {category.upper()}\n*Confidence:* {confidence * 100:.1f}%\n\n"
        
        # Add sentiment analysis
        if 'sentiment_analysis' in result:
            sentiment = result['sentiment_analysis']['sentiment']
            emoji_map = {'POSITIVE': '😊', 'NEGATIVE': '😞', 'NEUTRAL': '😐'}
            emoji = emoji_map.get(sentiment['label'], '🤔')
            response += f"{emoji} *Sentiment:* {sentiment['label']} ({sentiment['score'] * 100:.1f}%)\n"
            
            # Top emotions
            emotions = result['sentiment_analysis'].get('emotions', [])
            if emotions:
                top_emotions = ', '.join([f"{e['label']}" for e in emotions[:3]])
                response += f"*Emotions:* {top_emotions}\n"
        
        # Add metadata
        if 'metadata_analysis' in result:
            metadata = result['metadata_analysis']
            reading_time = metadata['reading_time']
            quality = metadata['quality_score']
            
            response += f"\n⏱️ *Reading Time:* {reading_time['formatted']}\n"
            response += f"📊 *Word Count:* {reading_time['word_count']}\n"
            response += f"⭐ *Quality:* {quality['score']}/100 ({quality['grade']})\n"
        
        # Add keywords
        if 'keyword_analysis' in result:
            keywords = result['keyword_analysis']['keywords'][:5]
            keyword_list = ', '.join([kw['word'] for kw in keywords])
            response += f"\n🔑 *Keywords:* {keyword_list}\n"
            
            # Named entities
            entities = result['keyword_analysis']['entities'][:5]
            if entities:
                entity_list = ', '.join([f"{e['text']} ({e['type']})" for e in entities])
                response += f"🏷️ *Entities:* {entity_list}\n"
        
        response += f"\n*Summary:*\n{summary}\n\n"
        response += f"*Source:* {message_text}"
        
        await processing_msg.edit_text(response, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        logger.error(f"Error processing article: {str(e)}")
        await processing_msg.edit_text(f"❌ An error occurred: {str(e)}")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show database statistics."""
    try:
        stats = processor.get_statistics()
        
        if not stats:
            await update.message.reply_text("No statistics available.")
            return
        
        response = "📊 *Statistics*\n\n"
        response += f"Total Articles: {stats['total_articles']}\n\n"
        
        if stats.get('category_distribution'):
            response += "*Category Distribution:*\n"
            for category, count in sorted(stats['category_distribution'].items(), key=lambda x: x[1], reverse=True):
                response += f"• {category}: {count}\n"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def cached_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recently cached articles."""
    try:
        articles = processor.get_cached_articles(limit=5)
        
        if not articles:
            await update.message.reply_text("No cached articles found.")
            return
        
        response = "📚 *Recent Cached Articles*\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Untitled')[:50]
            category = article.get('classification', {}).get('top_label', 'N/A')
            response += f"{i}. *{title}*\n   Category: {category}\n\n"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error getting cached articles: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    """Start the bot."""
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
        print("Error: Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    # Create the Application
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("cached", cached_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    
    # Start the Bot
    logger.info("Starting enhanced bot...")
    print("Enhanced Bot is running. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
