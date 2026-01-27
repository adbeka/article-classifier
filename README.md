# Article Classifier & Summarizer 📰✨

A powerful, feature-rich news article classifier and summarizer that uses advanced NLP to automatically scrape, classify, analyze, and generate insights from news articles. Available as a REST API, Telegram bot, and Chrome extension.

## ✨ Features

### Core Features
- **🔍 Article Scraping**: Automatically extract content from news article URLs
- **🏷️ Topic Classification**: Classify articles into 10+ categories using zero-shot classification
- **📝 Smart Summarization**: Generate concise summaries using transformer models
- **🤖 Telegram Bot**: Interact via Telegram for easy mobile access
- **🌐 Chrome Extension**: Analyze articles directly from your browser
- **🔌 REST API**: Flask-based API for integration with other applications

### 🚀 New Advanced Features
- **😊 Sentiment Analysis**: Detect emotional tone (positive, negative, neutral) and specific emotions
- **🔑 Keyword Extraction**: Identify important keywords and key phrases
- **🏷️ Named Entity Recognition**: Extract people, organizations, and locations
- **⏱️ Reading Time**: Calculate estimated reading time
- **⭐ Quality Score**: Assess article quality (0-100 scale)
- **📊 Readability Analysis**: Flesch Reading Ease score and grade level
- **💾 Database Caching**: Fast retrieval of previously processed articles
- **📤 Export Functionality**: Export to JSON, CSV, Markdown, and HTML
- **📈 Statistics & Analytics**: Track processing metrics and trends

**📚 [View Detailed Features Guide](FEATURES.md)**

## Supported Article Categories

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

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Telegram Bot Token for Telegram bot functionality
- (Optional) Chrome browser for extension

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/adbeka/article-classifier.git
cd article-classifier
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your settings (especially TELEGRAM_BOT_TOKEN if using Telegram bot)
```

## Usage

### 1. Command Line Interface

Process a single article:

```python
from src.main import ArticleProcessor

processor = ArticleProcessor()
result = processor.process_url("https://www.bbc.com/news/technology-12345678")

print(f"Title: {result['title']}")
print(f"Category: {result['classification']['top_label']}")
print(f"Summary: {result['summary']}")
```

Or run the example:

```bash
python src/main.py
```

### 2. Flask API Server

Start the API server:

```bash
python src/api.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

**Process a single article**:
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

**Process multiple articles**:
```bash
curl -X POST http://localhost:5000/api/batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["url1", "url2"]}'
```

**Health check**:
```bash
curl http://localhost:5000/api/health
```

### 3. Telegram Bot

1. Create a Telegram bot using [@BotFather](https://t.me/botfather)
2. Copy the bot token to your `.env` file as `TELEGRAM_BOT_TOKEN`
3. Start the bot:

```bash
python src/telegram_bot.py
```

4. Open Telegram and search for your bot
5. Send `/start` to begin
6. Paste any news article URL to get analysis

#### Bot Commands

- `/start` - Show welcome message
- `/help` - Show help information
- Send any URL - Analyze the article

### 4. Chrome Extension

1. **Start the API server** (required for the extension):
```bash
python src/api.py
```

2. **Load the extension in Chrome**:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `chrome-extension` directory from this project

3. **Add icons** (optional):
   - Add icon files (icon16.png, icon48.png, icon128.png) to `chrome-extension/icons/`
   - Or use placeholder icons

4. **Use the extension**:
   - Navigate to any news article
   - Click the extension icon
   - Configure the API URL if needed (default: http://localhost:5000)
   - Click "Analyze Current Page"

## Project Structure

```
article-classifier/
├── src/
│   ├── __init__.py
│   ├── main.py           # Main application & processor
│   ├── scraper.py        # Article scraping module
│   ├── classifier.py     # NLP classification module
│   ├── summarizer.py     # Text summarization module
│   ├── config.py         # Configuration settings
│   ├── api.py            # Flask API server
│   └── telegram_bot.py   # Telegram bot interface
├── chrome-extension/
│   ├── manifest.json     # Extension manifest
│   ├── popup.html        # Extension popup UI
│   ├── popup.js          # Extension popup logic
│   ├── background.js     # Extension background script
│   └── icons/            # Extension icons
├── tests/                # Test files
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Configuration

All configuration is done via environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | Required for bot |
| `FLASK_HOST` | Flask API host | 0.0.0.0 |
| `FLASK_PORT` | Flask API port | 5000 |
| `FLASK_DEBUG` | Enable Flask debug mode | False |
| `CLASSIFIER_MODEL` | Hugging Face classifier model | facebook/bart-large-mnli |
| `SUMMARIZER_MODEL` | Hugging Face summarizer model | facebook/bart-large-cnn |
| `SUMMARY_MAX_LENGTH` | Maximum summary length | 130 |
| `SUMMARY_MIN_LENGTH` | Minimum summary length | 30 |

## Models

This project uses pre-trained models from Hugging Face:

- **Classification**: `facebook/bart-large-mnli` - Zero-shot classification
- **Summarization**: `facebook/bart-large-cnn` - Abstractive summarization

The models will be automatically downloaded on first use (~1-2GB).

## Requirements

See `requirements.txt` for full list of dependencies:

- `requests` - HTTP library
- `beautifulsoup4` - HTML parsing
- `transformers` - NLP models
- `torch` - PyTorch framework
- `python-telegram-bot` - Telegram bot API
- `flask` - Web framework
- `flask-cors` - CORS support
- `newspaper3k` - Article extraction
- `python-dotenv` - Environment variables

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Categories

Edit the `CLASSIFICATION_LABELS` in `src/config.py` to add more categories.

### Custom Models

You can use different models by setting environment variables:

```bash
export CLASSIFIER_MODEL=your-model-name
export SUMMARIZER_MODEL=your-model-name
```

## Troubleshooting

### Model Download Issues
If models fail to download, ensure you have a stable internet connection and sufficient disk space (~2GB).

### API Connection Issues
Make sure the Flask API is running before using the Chrome extension. Check the console for errors.

### Telegram Bot Not Responding
Verify your `TELEGRAM_BOT_TOKEN` is correct and the bot is running.

### Chrome Extension Not Working
Ensure:
1. The API server is running
2. The API URL in the extension matches your server
3. You're on a valid web page (not chrome:// pages)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Hugging Face for providing pre-trained models
- The open-source community for the excellent libraries used in this project

## Contact

For issues, questions, or suggestions, please open an issue on GitHub.