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
        "Welcome to Article Classifier & Summarizer Bot! 🤖\n\n"
        "Send me a news article URL and I will:\n"
        "• Scrape the article content\n"
        "• Classify it by topic\n"
        "• Generate a summary\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Show help information\n\n"
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
    processing_msg = await update.message.reply_text("🔄 Processing article...")
    
    try:
        # Process the URL
        result = processor.process_url(message_text)
        
        if 'error' in result:
            await processing_msg.edit_text(f"❌ Error: {result['error']}")
            return
        
        # Format the response
        category = result['classification']['top_label']
        confidence = result['classification']['top_score']
        title = result.get('title', 'N/A')
        summary = result.get('summary', 'N/A')
        
        response = (
            f"📰 *Article Analysis*\n\n"
            f"*Title:* {title}\n\n"
            f"*Category:* {category.upper()}\n"
            f"*Confidence:* {confidence * 100:.1f}%\n\n"
            f"*Summary:*\n{summary}\n\n"
            f"*Source:* {message_text}"
        )
        
        await processing_msg.edit_text(response, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        logger.error(f"Error processing article: {str(e)}")
        await processing_msg.edit_text(f"❌ An error occurred: {str(e)}")


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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    
    # Start the Bot
    logger.info("Starting bot...")
    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
