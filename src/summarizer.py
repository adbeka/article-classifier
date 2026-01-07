"""
Article summarizer module using NLP for text summarization.
"""
from transformers import pipeline
from typing import Dict
from src.config import Config


class ArticleSummarizer:
    """Summarizer for generating concise summaries of article text."""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the summarizer with a pre-trained model.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.summarizer = pipeline("summarization", model=model_name)
    
    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """
        Generate a summary of the given text.
        
        Args:
            text: The article text to summarize
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            
        Returns:
            Summarized text
        """
        # Split long text into chunks if needed
        max_input_length = Config.MAX_SUMMARIZER_INPUT_LENGTH
        words = text.split()
        
        if len(words) <= max_input_length:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        
        # Process in chunks for very long articles
        chunk_size = max_input_length
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        
        # Limit to first 3 chunks to avoid excessive processing
        chunks_to_process = chunks[:3]
        if not chunks_to_process:
            return ""
        
        summaries = []
        chunk_max_length = max(max_length // len(chunks_to_process), 1)
        chunk_min_length = max(min_length // len(chunks_to_process), 1)
        
        for chunk in chunks_to_process:
            summary = self.summarizer(chunk, max_length=chunk_max_length, min_length=chunk_min_length, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        return ' '.join(summaries)
    
    def summarize_article(self, article: Dict[str, str], max_length: int = 130, min_length: int = 30) -> Dict[str, str]:
        """
        Add a summary to an article dictionary.
        
        Args:
            article: Article dictionary with 'text' key
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            
        Returns:
            Article dictionary with added 'summary' key
        """
        text = article.get('text', '')
        if not text:
            article['summary'] = ''
            return article
        
        summary = self.summarize(text, max_length, min_length)
        article['summary'] = summary
        return article
