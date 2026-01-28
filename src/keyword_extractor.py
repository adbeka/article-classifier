"""
Keyword extraction and entity recognition module.
"""
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from typing import Dict, List, Set
import re
from collections import Counter


class KeywordExtractor:
    """Extractor for identifying keywords, key phrases, and named entities."""
    
    def __init__(self):
        """Initialize the keyword extractor with NER model."""
        try:
            # Named Entity Recognition model
            self.ner_pipeline = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple"
            )
            self.has_ner = True
        except Exception:
            self.ner_pipeline = None
            self.has_ner = False
        
        # Common stopwords for filtering
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> Set[str]:
        """Load common English stopwords."""
        return {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which',
            'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just',
            'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good',
            'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now',
            'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back',
            'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
            'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give',
            'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had',
            'were', 'said', 'did', 'having', 'may', 'should', 'am'
        }
    
    def extract_keywords_frequency(self, text: str, top_n: int = 15) -> List[Dict[str, any]]:
        """
        Extract keywords based on frequency analysis.
        
        Args:
            text: The article text
            top_n: Number of top keywords to return
            
        Returns:
            List of dictionaries with 'word' and 'frequency'
        """
        # Tokenize and clean
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stopwords and get frequency
        filtered_words = [w for w in words if w not in self.stopwords]
        word_freq = Counter(filtered_words)
        
        # Get top keywords
        top_keywords = [
            {'word': word, 'frequency': freq}
            for word, freq in word_freq.most_common(top_n)
        ]
        
        return top_keywords
    
    def extract_named_entities(self, text: str) -> List[Dict[str, any]]:
        """
        Extract named entities (people, organizations, locations) from text.
        
        Args:
            text: The article text
            
        Returns:
            List of named entities with their types and confidence scores
        """
        if not self.has_ner:
            return []
        
        # Limit text length to avoid processing issues
        words = text.split()[:512]
        text_truncated = ' '.join(words)
        
        if not text_truncated:
            return []
        
        try:
            entities = self.ner_pipeline(text_truncated)
            
            # Format entities
            formatted_entities = []
            seen_entities = set()
            
            for entity in entities:
                entity_text = entity['word']
                entity_type = entity['entity_group']
                
                # Avoid duplicates
                entity_key = (entity_text.lower(), entity_type)
                if entity_key not in seen_entities:
                    formatted_entities.append({
                        'text': entity_text,
                        'type': entity_type,
                        'score': round(entity['score'], 3)
                    })
                    seen_entities.add(entity_key)
            
            return formatted_entities
        except Exception as e:
            print(f"Error in NER: {str(e)}")
            return []
    
    def extract_key_phrases(self, text: str, min_length: int = 2, max_length: int = 4, top_n: int = 10) -> List[Dict[str, any]]:
        """
        Extract key phrases (n-grams) from text.
        
        Args:
            text: The article text
            min_length: Minimum phrase length in words
            max_length: Maximum phrase length in words
            top_n: Number of top phrases to return
            
        Returns:
            List of key phrases with frequency
        """
        # Tokenize
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        phrases_counter = Counter()
        
        # Extract n-grams
        for n in range(min_length, max_length + 1):
            for i in range(len(words) - n + 1):
                phrase_words = words[i:i+n]
                
                # Skip if contains stopwords at start or end
                if phrase_words[0] in self.stopwords or phrase_words[-1] in self.stopwords:
                    continue
                
                phrase = ' '.join(phrase_words)
                phrases_counter[phrase] += 1
        
        # Get top phrases (with frequency > 1)
        top_phrases = [
            {'phrase': phrase, 'frequency': freq}
            for phrase, freq in phrases_counter.most_common(top_n * 2)
            if freq > 1
        ][:top_n]
        
        return top_phrases
    
    def analyze_article(self, article: Dict[str, str]) -> Dict[str, str]:
        """
        Extract keywords and entities from an article.
        
        Args:
            article: Article dictionary with 'text' and 'title' keys
            
        Returns:
            Article dictionary with added 'keyword_analysis' key
        """
        text = article.get('text', '')
        
        keywords = self.extract_keywords_frequency(text, top_n=15)
        entities = self.extract_named_entities(text)
        key_phrases = self.extract_key_phrases(text, top_n=10)
        
        article['keyword_analysis'] = {
            'keywords': keywords,
            'entities': entities,
            'key_phrases': key_phrases
        }
        
        return article
