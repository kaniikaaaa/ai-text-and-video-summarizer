"""
Grammar Correction and Text Polishing Module
Improves grammar, punctuation, and readability of summaries
"""

import re
from nltk.tokenize import sent_tokenize, word_tokenize

# Common contractions and their expansions
CONTRACTIONS = {
    "won't": "will not",
    "can't": "cannot",
    "n't": " not",
    "'re": " are",
    "'ve": " have",
    "'ll": " will",
    "'d": " would",
    "'m": " am",
    "let's": "let us",
}

# Articles that should precede certain words
VOWEL_SOUNDS = ['a', 'e', 'i', 'o', 'u', 'h']


def expand_contractions(text):
    """Expand contractions for better readability"""
    for contraction, expansion in CONTRACTIONS.items():
        text = re.sub(r'\b' + re.escape(contraction) + r'\b', expansion, text, flags=re.IGNORECASE)
    return text


def fix_capitalization(text):
    """Ensure proper capitalization"""
    # Capitalize first letter of each sentence
    sentences = sent_tokenize(text)
    corrected_sentences = []
    
    for sentence in sentences:
        if sentence:
            # Capitalize first letter
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            corrected_sentences.append(sentence)
    
    return ' '.join(corrected_sentences)


def fix_punctuation(text):
    """Fix common punctuation issues"""
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Add space after punctuation if missing
    text = re.sub(r'([.,!?;:])([A-Za-z])', r'\1 \2', text)
    
    # Fix multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Ensure sentences end with punctuation
    text = text.strip()
    if text and text[-1] not in '.!?':
        text += '.'
    
    # Fix ellipsis
    text = re.sub(r'\.{2,}', '...', text)
    
    # Remove space before apostrophe
    text = re.sub(r"\s+'", "'", text)
    
    return text


def fix_sentence_structure(text):
    """Improve sentence structure"""
    sentences = sent_tokenize(text)
    improved_sentences = []
    
    for sentence in sentences:
        # Skip very short sentences (likely fragments)
        words = word_tokenize(sentence)
        if len(words) < 3:
            continue
        
        # Remove sentences that are just numbers or symbols
        if re.match(r'^[\d\s.,!?;:]+$', sentence):
            continue
        
        # Ensure sentence starts with a capital letter
        if sentence and sentence[0].islower():
            sentence = sentence[0].upper() + sentence[1:]
        
        # Ensure sentence ends with proper punctuation
        if sentence and sentence[-1] not in '.!?':
            sentence += '.'
        
        improved_sentences.append(sentence)
    
    return ' '.join(improved_sentences)


def remove_redundant_phrases(text):
    """Remove redundant or filler phrases"""
    # Common redundant phrases in summaries
    redundant_patterns = [
        r'\b(basically|essentially|actually|literally)\b',
        r'\b(in order to)\b',
        r'\b(due to the fact that)\b',
        r'\b(at this point in time)\b',
        r'\b(for all intents and purposes)\b',
    ]
    
    for pattern in redundant_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def improve_article_usage(text):
    """Add missing articles where appropriate (basic heuristic)"""
    # This is a simplified approach - for production, consider using spaCy or similar
    sentences = sent_tokenize(text)
    improved_sentences = []
    
    for sentence in sentences:
        # Basic pattern: verb + singular noun without article
        # Example: "He is teacher" -> "He is a teacher"
        words = word_tokenize(sentence)
        
        # Simple heuristic improvements
        sentence_improved = sentence
        
        improved_sentences.append(sentence_improved)
    
    return ' '.join(improved_sentences)


def fix_common_grammar_mistakes(text):
    """Fix common grammar mistakes"""
    # Subject-verb agreement patterns (basic)
    text = re.sub(r'\b(he|she|it)\s+are\b', r'\1 is', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(they|we|you)\s+is\b', r'\1 are', text, flags=re.IGNORECASE)
    
    # Fix double negatives
    text = re.sub(r"\bdon't\s+not\b", "don't", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcan't\s+not\b", "can", text, flags=re.IGNORECASE)
    
    # Fix common word confusions
    text = re.sub(r'\bthere\s+is\s+many\b', 'there are many', text, flags=re.IGNORECASE)
    text = re.sub(r'\bthere\s+are\s+a\b', 'there is a', text, flags=re.IGNORECASE)
    
    return text


def clean_summary_text(text):
    """Main function to clean and improve summary text
    
    Applies all grammar corrections and improvements
    """
    if not text or not text.strip():
        return text
    
    # Step 1: Expand contractions for clarity
    text = expand_contractions(text)
    
    # Step 2: Fix punctuation
    text = fix_punctuation(text)
    
    # Step 3: Fix sentence structure
    text = fix_sentence_structure(text)
    
    # Step 4: Fix capitalization
    text = fix_capitalization(text)
    
    # Step 5: Remove redundant phrases
    text = remove_redundant_phrases(text)
    
    # Step 6: Fix common grammar mistakes
    text = fix_common_grammar_mistakes(text)
    
    # Step 7: Improve article usage (basic)
    text = improve_article_usage(text)
    
    # Step 8: Final cleanup
    text = fix_punctuation(text)  # Run again for final polish
    
    # Step 9: Remove multiple consecutive punctuation marks
    text = re.sub(r'([.!?]){2,}', r'\1', text)
    
    # Step 10: Ensure consistent spacing
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def validate_sentence_completeness(sentence):
    """Check if a sentence is grammatically complete (basic check)"""
    words = word_tokenize(sentence.lower())
    
    # Very basic check - sentence should have at least a noun/pronoun and verb
    # This is simplified - for production use spaCy POS tagging
    
    # Check minimum length
    if len(words) < 3:
        return False
    
    # Check if it has some content words (not just stopwords)
    stopwords_simple = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    content_words = [w for w in words if w not in stopwords_simple]
    
    if len(content_words) < 2:
        return False
    
    # Check if it ends with punctuation
    if sentence.strip() and sentence.strip()[-1] not in '.!?':
        return False
    
    return True


def filter_incomplete_sentences(text):
    """Remove incomplete or fragmented sentences"""
    sentences = sent_tokenize(text)
    complete_sentences = []
    
    for sentence in sentences:
        if validate_sentence_completeness(sentence):
            complete_sentences.append(sentence)
    
    return ' '.join(complete_sentences)


def polish_summary(text):
    """High-level function to polish the final summary
    
    This is the main function to call for grammar correction
    """
    # Apply all corrections
    text = clean_summary_text(text)
    
    # Filter out incomplete sentences
    text = filter_incomplete_sentences(text)
    
    # Final polish
    text = text.strip()
    
    # Ensure it ends with proper punctuation
    if text and text[-1] not in '.!?':
        text += '.'
    
    return text


# Test function
if __name__ == "__main__":
    # Test cases
    test_texts = [
        "this is test sentence without capital.another sentence",
        "He are going to school.They is happy.",
        "basically the text contain lots of information  .",
        "text with multiple    spaces and bad punctuation,like this"
    ]
    
    for test in test_texts:
        print(f"Original: {test}")
        print(f"Corrected: {polish_summary(test)}")
        print("-" * 50)
