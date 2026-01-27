"""
Article metadata analyzer for calculating reading time, quality metrics, and other metadata.
"""
import re
from typing import Dict, List
from datetime import datetime
import math


class MetadataAnalyzer:
    """Analyzer for article metadata including reading time, quality score, and statistics."""
    
    def __init__(self):
        """Initialize the metadata analyzer."""
        self.avg_reading_speed = 200  # words per minute (average adult reading speed)
    
    def calculate_reading_time(self, text: str) -> Dict[str, any]:
        """
        Calculate estimated reading time for the article.
        
        Args:
            text: The article text
            
        Returns:
            Dictionary with reading time in minutes and formatted string
        """
        word_count = len(text.split())
        minutes = math.ceil(word_count / self.avg_reading_speed)
        
        if minutes < 1:
            return {
                'minutes': 1,
                'formatted': 'Less than 1 minute',
                'word_count': word_count
            }
        elif minutes == 1:
            return {
                'minutes': 1,
                'formatted': '1 minute read',
                'word_count': word_count
            }
        else:
            return {
                'minutes': minutes,
                'formatted': f'{minutes} minutes read',
                'word_count': word_count
            }
    
    def calculate_readability_score(self, text: str) -> Dict[str, any]:
        """
        Calculate readability score using Flesch Reading Ease formula.
        
        Args:
            text: The article text
            
        Returns:
            Dictionary with readability score and interpretation
        """
        # Count sentences
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        if sentence_count == 0:
            return {
                'score': 0,
                'interpretation': 'Unknown',
                'grade_level': 'Unknown'
            }
        
        # Count words and syllables
        words = text.split()
        word_count = len(words)
        
        if word_count == 0:
            return {
                'score': 0,
                'interpretation': 'Unknown',
                'grade_level': 'Unknown'
            }
        
        syllable_count = sum(self._count_syllables(word) for word in words)
        
        # Flesch Reading Ease Score
        # Score = 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        try:
            score = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
            score = max(0, min(100, score))  # Clamp between 0 and 100
        except ZeroDivisionError:
            score = 0
        
        # Interpret score
        if score >= 90:
            interpretation = "Very Easy"
            grade_level = "5th grade"
        elif score >= 80:
            interpretation = "Easy"
            grade_level = "6th grade"
        elif score >= 70:
            interpretation = "Fairly Easy"
            grade_level = "7th grade"
        elif score >= 60:
            interpretation = "Standard"
            grade_level = "8th-9th grade"
        elif score >= 50:
            interpretation = "Fairly Difficult"
            grade_level = "10th-12th grade"
        elif score >= 30:
            interpretation = "Difficult"
            grade_level = "College"
        else:
            interpretation = "Very Difficult"
            grade_level = "College Graduate"
        
        return {
            'score': round(score, 1),
            'interpretation': interpretation,
            'grade_level': grade_level
        }
    
    def _count_syllables(self, word: str) -> int:
        """
        Estimate syllable count for a word.
        
        Args:
            word: The word to count syllables for
            
        Returns:
            Estimated syllable count
        """
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        # Ensure at least 1 syllable
        if syllable_count == 0:
            syllable_count = 1
        
        return syllable_count
    
    def calculate_quality_score(self, article: Dict[str, any]) -> Dict[str, any]:
        """
        Calculate an overall quality score for the article.
        
        Args:
            article: Article dictionary
            
        Returns:
            Dictionary with quality score and breakdown
        """
        score = 0
        max_score = 100
        breakdown = {}
        
        text = article.get('text', '')
        word_count = len(text.split())
        
        # 1. Length score (0-25 points)
        if word_count >= 300:
            length_score = 25
        elif word_count >= 150:
            length_score = 20
        elif word_count >= 100:
            length_score = 15
        else:
            length_score = 10
        
        breakdown['length_score'] = length_score
        score += length_score
        
        # 2. Has title (0-15 points)
        title_score = 15 if article.get('title', '').strip() else 0
        breakdown['title_score'] = title_score
        score += title_score
        
        # 3. Has author (0-10 points)
        authors = article.get('authors', [])
        author_score = 10 if authors and len(authors) > 0 else 0
        breakdown['author_score'] = author_score
        score += author_score
        
        # 4. Has publish date (0-10 points)
        date_score = 10 if article.get('publish_date') else 0
        breakdown['date_score'] = date_score
        score += date_score
        
        # 5. Readability (0-20 points)
        if text:
            readability = self.calculate_readability_score(text)
            readability_score = readability['score'] / 5  # Convert 0-100 to 0-20
            breakdown['readability_score'] = round(readability_score, 1)
            score += readability_score
        else:
            breakdown['readability_score'] = 0
        
        # 6. Structure (0-20 points)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        
        structure_score = 0
        if sentence_count >= 5:
            structure_score += 10
        if paragraph_count >= 2:
            structure_score += 10
        
        breakdown['structure_score'] = structure_score
        score += structure_score
        
        # Normalize to 0-100
        quality_percentage = (score / max_score) * 100
        
        # Grade interpretation
        if quality_percentage >= 90:
            grade = 'Excellent'
        elif quality_percentage >= 80:
            grade = 'Very Good'
        elif quality_percentage >= 70:
            grade = 'Good'
        elif quality_percentage >= 60:
            grade = 'Fair'
        else:
            grade = 'Poor'
        
        return {
            'score': round(quality_percentage, 1),
            'grade': grade,
            'breakdown': breakdown
        }
    
    def get_text_statistics(self, text: str) -> Dict[str, any]:
        """
        Get detailed text statistics.
        
        Args:
            text: The article text
            
        Returns:
            Dictionary with various text statistics
        """
        words = text.split()
        word_count = len(words)
        
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        avg_word_length = char_count_no_spaces / word_count if word_count > 0 else 0
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'average_word_length': round(avg_word_length, 1),
            'average_sentence_length': round(avg_sentence_length, 1)
        }
    
    def analyze_article(self, article: Dict[str, any]) -> Dict[str, any]:
        """
        Perform comprehensive metadata analysis on an article.
        
        Args:
            article: Article dictionary
            
        Returns:
            Article dictionary with added 'metadata_analysis' key
        """
        text = article.get('text', '')
        
        reading_time = self.calculate_reading_time(text)
        readability = self.calculate_readability_score(text)
        quality_score = self.calculate_quality_score(article)
        text_stats = self.get_text_statistics(text)
        
        article['metadata_analysis'] = {
            'reading_time': reading_time,
            'readability': readability,
            'quality_score': quality_score,
            'text_statistics': text_stats,
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        return article
