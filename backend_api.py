from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import io
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import ssl
import re

# Fix SSL certificate issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download necessary NLTK resources
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize the summarization model (using transformers)
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    USE_TRANSFORMER = True
except Exception as e:
    print(f"Could not load transformer model: {e}")
    USE_TRANSFORMER = False

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + " "
        # Clean up extracted text
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = text.strip()
        return text
    except Exception as e:
        return None

def clean_text(text):
    """Clean and preprocess text"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\'"()\-]', '', text)
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return text.strip()

def preprocess_text_for_sentences(text):
    """Preprocess text to handle comma-separated clauses as separate sentences"""
    # Replace commas followed by space with periods for better sentence splitting
    # This helps when input is like "clause1, clause2, clause3"
    text = re.sub(r',\s+', '. ', text)
    # Ensure sentences end with period
    if not text.endswith('.'):
        text += '.'
    # Clean up multiple periods
    text = re.sub(r'\.+', '.', text)
    # Fix spacing
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def calculate_optimal_summary_length(text):
    """
    Automatically calculate optimal summary length based on input text characteristics
    Returns optimal number of sentences for summary
    """
    # Get text statistics
    sentences = sent_tokenize(text)
    words = text.split()
    
    num_sentences = len(sentences)
    num_words = len(words)
    avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
    
    # Strategy 1: Based on total word count
    if num_words < 100:
        # Very short text - preserve most of it
        target_sentences = max(2, int(num_sentences * 0.7))
    elif num_words < 300:
        # Short text - 50-60% retention
        target_sentences = max(2, int(num_sentences * 0.5))
    elif num_words < 800:
        # Medium text - 30-40% retention
        target_sentences = max(3, int(num_sentences * 0.35))
    elif num_words < 2000:
        # Long text - 20-30% retention
        target_sentences = max(4, int(num_sentences * 0.25))
    else:
        # Very long text - 15-20% retention
        target_sentences = max(5, int(num_sentences * 0.18))
    
    # Strategy 2: Adjust based on sentence complexity
    if avg_sentence_length > 25:
        # Complex sentences - can reduce more
        target_sentences = max(2, int(target_sentences * 0.8))
    elif avg_sentence_length < 10:
        # Simple sentences - need more to convey meaning
        target_sentences = int(target_sentences * 1.2)
    
    # Strategy 3: Ensure reasonable bounds
    target_sentences = max(2, min(target_sentences, 12))  # Between 2-12 sentences
    
    # Don't exceed original sentence count
    target_sentences = min(target_sentences, num_sentences)
    
    return target_sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    """Compute similarity between two sentences"""
    if stopwords is None:
        stopwords = []
   
    sent1 = [word for word in sent1 if word not in stopwords]
    sent2 = [word for word in sent2 if word not in stopwords]
   
    all_words = list(set(sent1 + sent2))
   
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    
    for word in sent1:
        if word in all_words:
            vector1[all_words.index(word)] += 1
    for word in sent2:
        if word in all_words:
            vector2[all_words.index(word)] += 1
   
    if sum(vector1) == 0 or sum(vector2) == 0:
        return 0
    
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    """Build a similarity matrix for all sentences"""
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)
   
    return similarity_matrix

def calculate_sentence_importance(sentences, stop_words):
    """Calculate importance scores for sentences using advanced multi-factor analysis"""
    scores = {}
    n_sentences = len(sentences)
    
    # 1. TF-IDF scores - Most important for content relevance
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english', 
            max_features=200,
            ngram_range=(1, 2),  # Include bigrams for better context
            min_df=1,
            max_df=0.85
        )
        tfidf_matrix = vectorizer.fit_transform(sentences)
        tfidf_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        # Normalize
        if tfidf_scores.max() > 0:
            tfidf_scores = tfidf_scores / tfidf_scores.max()
    except:
        tfidf_scores = np.ones(n_sentences)
    
    # 2. Enhanced Position scores
    position_scores = np.zeros(n_sentences)
    for i in range(n_sentences):
        if i == 0:
            position_scores[i] = 3.0  # First sentence - critical
        elif i == 1:
            position_scores[i] = 2.0  # Second sentence - very important
        elif i < min(5, n_sentences * 0.1):
            position_scores[i] = 1.5  # Early sentences
        elif i >= n_sentences - 1:
            position_scores[i] = 1.8  # Last sentence - often conclusion
        elif i >= n_sentences - 3:
            position_scores[i] = 1.3  # Near end
        else:
            position_scores[i] = 1.0  # Middle
    
    # 3. Length scores - Prefer informative sentences
    length_scores = np.zeros(n_sentences)
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence)
        word_count = len(words)
        if 12 <= word_count <= 25:  # Sweet spot
            length_scores[i] = 2.0
        elif 8 <= word_count <= 35:  # Acceptable
            length_scores[i] = 1.5
        elif 5 <= word_count <= 45:  # Ok
            length_scores[i] = 1.0
        else:  # Too short or too long
            length_scores[i] = 0.5
    
    # 4. Enhanced Keyword and Feature scores
    keyword_scores = np.zeros(n_sentences)
    discourse_markers = [
        'however', 'therefore', 'thus', 'consequently', 'moreover', 'furthermore',
        'importantly', 'significantly', 'notably', 'essentially', 'primarily',
        'specifically', 'particularly', 'especially', 'indeed', 'in fact',
        'for example', 'for instance', 'in conclusion', 'to summarize', 'overall'
    ]
    
    for i, sentence in enumerate(sentences):
        score = 1.0
        sentence_lower = sentence.lower()
        
        # Numbers (facts, statistics)
        num_count = len(re.findall(r'\d+', sentence))
        if num_count > 0:
            score += min(num_count * 0.3, 0.9)
        
        # Proper nouns (entities, names)
        capitals = len(re.findall(r'\b[A-Z][a-z]+', sentence))
        if capitals > 0:
            score += min(capitals * 0.15, 0.6)
        
        # Quotation marks (direct quotes)
        if '"' in sentence or '"' in sentence or "'" in sentence:
            score += 0.4
        
        # Discourse markers (signal importance)
        for marker in discourse_markers:
            if marker in sentence_lower:
                score += 0.5
                break
        
        # Questions (often frame key issues)
        if '?' in sentence:
            score += 0.3
        
        # Superlatives and emphasis words
        emphasis_words = ['most', 'best', 'worst', 'largest', 'smallest', 'critical', 
                         'essential', 'key', 'main', 'major', 'significant', 'important']
        for word in emphasis_words:
            if re.search(r'\b' + word + r'\b', sentence_lower):
                score += 0.2
                break
        
        keyword_scores[i] = score
    
    # 5. Centrality scores (TextRank-style graph)
    processed_sentences = [word_tokenize(s.lower()) for s in sentences]
    similarity_matrix = build_similarity_matrix(processed_sentences, stop_words)
    
    # Calculate eigenvector centrality (better than simple sum)
    centrality_scores = np.zeros(n_sentences)
    if similarity_matrix.max() > 0:
        # Normalize similarity matrix
        row_sums = similarity_matrix.sum(axis=1)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        norm_matrix = similarity_matrix / row_sums[:, np.newaxis]
        
        # Power iteration for centrality
        centrality = np.ones(n_sentences) / n_sentences
        for _ in range(10):  # 10 iterations usually enough
            centrality = 0.85 * norm_matrix.T.dot(centrality) + 0.15 / n_sentences
        
        centrality_scores = centrality / centrality.max() if centrality.max() > 0 else centrality
    
    # 6. Diversity penalty - Reduce score for very similar sentences already selected
    diversity_scores = np.ones(n_sentences)
    
    # Combine all scores with optimized weights
    for i in range(n_sentences):
        combined_score = (
            tfidf_scores[i] * 3.0 +           # Content relevance - highest weight
            centrality_scores[i] * 2.5 +      # Centrality - very important
            position_scores[i] * 2.0 +        # Position - important
            keyword_scores[i] * 1.5 +         # Keywords and features
            length_scores[i] * 1.0 +          # Length preference
            diversity_scores[i] * 0.5         # Diversity bonus
        )
        scores[i] = combined_score
    
    return scores

def are_sentences_similar(sent1, sent2, threshold=0.7):
    """Check if two sentences are too similar"""
    words1 = set(word_tokenize(sent1.lower()))
    words2 = set(word_tokenize(sent2.lower()))
    
    if len(words1) == 0 or len(words2) == 0:
        return False
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    similarity = intersection / union if union > 0 else 0
    return similarity > threshold

def textrank_summarize(text, max_sentences=None):
    """Generate summary using advanced TextRank with redundancy removal
    
    Args:
        text: Input text to summarize
        max_sentences: Maximum sentences in summary. If None, automatically calculated.
    """
    stop_words = set(stopwords.words("english"))
    
    # Preprocess text to handle comma-separated clauses
    text = preprocess_text_for_sentences(text)
    
    # Clean the text
    text = clean_text(text)
    
    # Auto-calculate optimal summary length if not provided
    if max_sentences is None or max_sentences == 0:
        max_sentences = calculate_optimal_summary_length(text)
        print(f"Auto-calculated summary length: {max_sentences} sentences")
    
    # Get original sentences
    original_sentences = sent_tokenize(text)
    
    # Step 1: Remove exact duplicates first (preserve order of first occurrence)
    seen_sentences = {}
    unique_sentences = []
    for idx, sentence in enumerate(original_sentences):
        normalized = sentence.strip().lower()
        if normalized not in seen_sentences:
            seen_sentences[normalized] = idx
            unique_sentences.append(sentence.strip())
    
    # Step 2: Filter sentences by length and quality
    filtered_sentences = []
    for sentence in unique_sentences:
        words = word_tokenize(sentence)
        # Keep sentences with at least 3 words (relaxed from 5)
        if 3 <= len(words) <= 50:
            # Remove sentences that are likely headers or titles (all caps, very short)
            if not (sentence.isupper() and len(words) < 4):
                filtered_sentences.append(sentence)
    
    if len(filtered_sentences) == 0:
        return "Unable to generate summary."
    
    # If unique sentences are already less than or equal to max, return them all
    if len(filtered_sentences) <= max_sentences:
        return " ".join(filtered_sentences)
    
    # Step 3: Calculate importance scores
    sentence_scores = calculate_sentence_importance(filtered_sentences, stop_words)
    
    # Step 4: Select diverse sentences (avoid very similar ones)
    selected_sentences = []
    selected_indices = []
    
    # Sort by score
    ranked_items = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    
    for idx, score in ranked_items:
        if len(selected_indices) >= max_sentences:
            break
        
        sentence = filtered_sentences[idx]
        
        # Check if this sentence is too similar to already selected ones
        is_redundant = False
        for selected_idx in selected_indices:
            # Use stricter threshold (0.5 instead of 0.6) for better duplicate detection
            if are_sentences_similar(sentence, filtered_sentences[selected_idx], threshold=0.5):
                is_redundant = True
                break
        
        if not is_redundant:
            selected_indices.append(idx)
            selected_sentences.append(sentence)
    
    # If we don't have enough sentences due to redundancy, add more with lower scores
    if len(selected_indices) < max_sentences:
        for idx, score in ranked_items:
            if len(selected_indices) >= max_sentences:
                break
            if idx not in selected_indices:
                selected_indices.append(idx)
                selected_sentences.append(filtered_sentences[idx])
    
    # Sort by original order to maintain coherence
    sorted_pairs = sorted(zip(selected_indices, selected_sentences), key=lambda x: x[0])
    final_sentences = [sent for _, sent in sorted_pairs]
    
    summary = " ".join(final_sentences)
    
    # Final cleanup
    summary = re.sub(r'\s+', ' ', summary).strip()
    
    return summary

def transformer_summarize(text, max_sentences=None):
    """Generate summary using transformer model with intelligent chunking
    
    Args:
        text: Input text to summarize
        max_sentences: Target sentences in summary. If None, automatically calculated.
    """
    try:
        # Clean the text
        text = text.strip()
        
        # Auto-calculate optimal summary length if not provided
        if max_sentences is None or max_sentences == 0:
            max_sentences = calculate_optimal_summary_length(text)
            print(f"Auto-calculated summary length (Transformer): {max_sentences} sentences")
        
        # Calculate dynamic lengths based on input
        words = text.split()
        input_length = len(words)
        
        # Adjust output length based on input and desired sentences
        # Aim for roughly 15-25 words per sentence
        target_words = max_sentences * 20
        max_length = min(target_words + 20, int(input_length * 0.4))  # Max 40% of input
        min_length = min(target_words - 10, int(input_length * 0.1))  # Min 10% of input
        
        # Ensure reasonable bounds
        max_length = max(50, min(max_length, 500))
        min_length = max(30, min(min_length, max_length - 20))
        
        # If text is too long, use intelligent extraction first
        if input_length > 1024:
            # Use TextRank to extract most important content first
            sentences = sent_tokenize(text)
            if len(sentences) > max_sentences * 3:
                # Extract top sentences using TextRank first
                stop_words = stopwords.words("english")
                scores = calculate_sentence_importance(sentences, stop_words)
                top_indices = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)[:max_sentences * 3]
                top_indices = sorted(top_indices)  # Maintain order
                text = " ".join([sentences[i] for i in top_indices])
                words = text.split()
        
        # Limit to model's capacity
        if len(words) > 1024:
            text = ' '.join(words[:1024])
        
        # Generate summary with optimized parameters
        summary = summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length,
            do_sample=False,
            truncation=True,
            length_penalty=2.0,  # Encourage appropriate length
            num_beams=4,          # Better quality with beam search
            early_stopping=True
        )
        
        result = summary[0]['summary_text']
        
        # Post-process: ensure proper formatting
        result = result.strip()
        if not result.endswith('.'):
            result += '.'
        
        return result
        
    except Exception as e:
        print(f"Transformer summarization failed: {e}")
        return None

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """API endpoint for text summarization"""
    try:
        text = ""
        
        # Check if file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename.endswith('.pdf'):
                # Extract text from PDF
                text = extract_text_from_pdf(file)
                if not text:
                    return jsonify({'error': 'Could not extract text from PDF'}), 400
            elif file.filename.endswith('.txt'):
                # Read text file
                text = file.read().decode('utf-8')
            else:
                return jsonify({'error': 'Unsupported file format. Please upload PDF or TXT file'}), 400
        
        # Check if text is provided directly
        elif request.json and 'text' in request.json:
            text = request.json['text']
        else:
            return jsonify({'error': 'No text or file provided'}), 400
        
        if not text or not text.strip():
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Get summary parameters from form (if file upload) or json (if text)
        if 'file' in request.files:
            method = request.form.get('method', 'textrank')
            max_sentences_str = request.form.get('max_sentences', 'auto')
            max_sentences = None if max_sentences_str == 'auto' or max_sentences_str == '' else int(max_sentences_str)
        elif request.json:
            method = request.json.get('method', 'textrank')
            max_sentences_value = request.json.get('max_sentences', 'auto')
            max_sentences = None if max_sentences_value == 'auto' or max_sentences_value == '' or max_sentences_value is None else int(max_sentences_value)
        else:
            method = 'textrank'
            max_sentences = None
        
        # Generate summary
        if method == 'transformer' and USE_TRANSFORMER:
            summary = transformer_summarize(text, max_sentences)
            if not summary:
                # Fallback to TextRank
                summary = textrank_summarize(text, max_sentences)
        else:
            summary = textrank_summarize(text, max_sentences)
        
        # Calculate stats
        original_words = len(text.split())
        summary_words = len(summary.split())
        compression_ratio = round((1 - summary_words/original_words) * 100, 1)
        
        return jsonify({
            'original_text': text,
            'summary': summary,
            'original_word_count': original_words,
            'summary_word_count': summary_words,
            'compression_ratio': compression_ratio
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'transformer_available': USE_TRANSFORMER})

if __name__ == '__main__':
    print("Starting Text Summarizer API...")
    print(f"Transformer model available: {USE_TRANSFORMER}")
    app.run(debug=True, port=5000, host='0.0.0.0')
