# Quick Start Guide

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher installed
- pip package manager
- At least 3GB of free disk space (for ML models)
- Stable internet connection (for first-time model download)

## Installation Steps

### 1. Clone and Setup

```bash
git clone https://github.com/adbeka/article-classifier.git
cd article-classifier
pip install -r requirements.txt
```

**Note**: Installation may take 5-10 minutes as it downloads PyTorch and transformer models.

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Telegram bot token (if using Telegram bot):
```
TELEGRAM_BOT_TOKEN=your_token_here
```

Get a token from [@BotFather](https://t.me/botfather) on Telegram.

## Usage Examples

### Option 1: Command Line (Simplest)

Create a file `test_article.py`:

```python
from src.main import ArticleProcessor

processor = ArticleProcessor()

# Process a news article
url = "https://www.bbc.com/news/technology-67890123"  # Use a real URL
result = processor.process_url(url)

print(f"Title: {result['title']}")
print(f"Category: {result['classification']['top_label']}")
print(f"Confidence: {result['classification']['top_score']:.2%}")
print(f"\nSummary:\n{result['summary']}")
```

Run it:
```bash
python test_article.py
```

### Option 2: Flask API Server

1. Start the server:
```bash
python src/api.py
```

2. In another terminal, test the API:
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/technology-67890123"}'
```

### Option 3: Telegram Bot

1. Get a bot token from [@BotFather](https://t.me/botfather)
2. Add it to your `.env` file
3. Start the bot:
```bash
python src/telegram_bot.py
```
4. Open Telegram and chat with your bot
5. Send any news article URL

### Option 4: Chrome Extension

1. Start the Flask API server:
```bash
python src/api.py
```

2. Load the extension in Chrome:
   - Go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `chrome-extension` folder

3. Navigate to any news article and click the extension icon

## Testing Your Installation

Run the unit tests:
```bash
pytest tests/
```

**Note**: Tests will fail if dependencies aren't installed. Install with:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### "Model not found" errors
The models will automatically download on first use. Ensure you have internet access and sufficient disk space (~2GB).

### "CUDA out of memory" errors
The models will automatically use CPU if GPU isn't available. CPU inference is slower but works fine.

### API connection issues
Make sure the Flask server is running on port 5000 before using the Chrome extension.

### Telegram bot not responding
- Verify your token is correct in `.env`
- Make sure the bot script is running
- Check that you haven't exceeded Telegram's rate limits

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Customize classification categories in `src/config.py`
- Try different summarization models
- Add more news sources

## Support

For issues or questions, open an issue on GitHub.
