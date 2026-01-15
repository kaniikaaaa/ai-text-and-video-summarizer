import nltk
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("punkt")

# Function to process the text into sentences and words
def read_article(text):
    sentences = sent_tokenize(text)
    return [word_tokenize(sentence.lower()) for sentence in sentences]

# Compute similarity between two sentences
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
   
    # Remove stopwords
    sent1 = [word for word in sent1 if word not in stopwords]
    sent2 = [word for word in sent2 if word not in stopwords]
   
    # Create a list of unique words from both sentences
    all_words = list(set(sent1 + sent2))
   
    # Create word frequency vectors for both sentences
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    
    for word in sent1:
        vector1[all_words.index(word)] += 1
    for word in sent2:
        vector2[all_words.index(word)] += 1
   
    # Compute cosine similarity
    return 1 - cosine_distance(vector1, vector2)

# Build a similarity matrix for all sentences
def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)
   
    return similarity_matrix

# Generate the summary
def generate_summary(text, word_limit=50):
    # Load stopwords
    stop_words = stopwords.words("english")
   
    # Process the text into sentences
    sentences = read_article(text)
    
    # Build the sentence similarity matrix
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)
   
    # Rank sentences based on their similarity scores
    sentence_similarity_graph = np.sum(sentence_similarity_matrix, axis=1)
    ranked_sentence_indices = np.argsort(-sentence_similarity_graph)  # Sort in descending order
   
    # Extract sentences for the summary until the word limit is reached
    original_sentences = sent_tokenize(text)
    summary_sentences = []
    word_count = 0

    for index in ranked_sentence_indices:
        sentence = original_sentences[index]
        words_in_sentence = len(word_tokenize(sentence))
        if word_count + words_in_sentence <= word_limit:
            summary_sentences.append(sentence)
            word_count += words_in_sentence
        if word_count >= word_limit:
            break

    return " ".join(summary_sentences)

# Feature extraction function
def extract_features(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = stopwords.words("english")
    
    # Remove stopwords and punctuation
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Count unique words
    unique_words = set(filtered_words)
    
    # Count word frequency
    word_freq = Counter(filtered_words)
    
    # Calculate average sentence length
    avg_sentence_length = len(words) / len(sentences) if sentences else 0

    # Features
    features = {
        "Total Words": len(words),
        "Total Sentences": len(sentences),
        "Unique Words": len(unique_words),
        "Most Common Words": word_freq.most_common(5),
        "Average Sentence Length": avg_sentence_length
    }
    
    return features

# Example usage with user input
text = input("Enter the text you want to summarize:\n")
word_limit = int(input("Enter the total number of words for the summary: "))

# Generate and display the summary
summary = generate_summary(text, word_limit=word_limit)
features = extract_features(text)

# Output
print("\nOriginal Text:\n", text)
print("\nSummary:\n", summary)
