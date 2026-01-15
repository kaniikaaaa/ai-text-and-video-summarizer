#tf-idf,bow,sentence position
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from sentence_transformers import SentenceTransformer
import numpy as np
import requests
import certifi
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

# Function to fetch and clean text from a URL
def fetch_text_from_url(url):
    response = requests.get(url, verify=certifi.where())
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    sentences = sent_tokenize(text)  # Tokenize text into sentences
    return sentences

# Example usage with your existing feature extraction code
url = "https://www.bbc.com/news/world"  
sentences = fetch_text_from_url(url)


# 1. TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
tfidf_array = tfidf_matrix.toarray()

# 2. Bag of Words (BoW)
bow_vectorizer = CountVectorizer()
bow_matrix = bow_vectorizer.fit_transform(sentences)
bow_array = bow_matrix.toarray()

# 3. Sentence Position
sentence_positions = np.array([i for i in range(len(sentences))]).reshape(-1, 1)

# 4. Sentence Length (in terms of word count)
sentence_lengths = np.array([len(word_tokenize(sentence)) for sentence in sentences]).reshape(-1, 1)

# 5. POS Tagging (Count of Nouns as a simple feature)
noun_counts = np.array([sum(1 for word, pos in pos_tag(word_tokenize(sentence)) if pos.startswith('NN')) for sentence in sentences]).reshape(-1, 1)

# 6. Sentence Embeddings (using Sentence-BERT)
model = SentenceTransformer('all-MiniLM-L6-v2')
sentence_embeddings = model.encode(sentences) 

# Combining all features into one feature matrix
combined_features = np.hstack((tfidf_array, bow_array, sentence_positions,sentence_lengths,noun_counts,sentence_embeddings))
print("\nCombined Feature Matrix:")
print(combined_features)
