"""
Video Summarization API with Timestamp Detection
Extracts transcript from YouTube videos, summarizes content, and detects topic changes
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
from urllib.parse import urlparse, parse_qs
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)


def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    # Handle different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def get_youtube_transcript(video_url):
    """
    Extract transcript from YouTube video with timestamps
    Returns list of transcript segments with text and timestamps
    """
    try:
        video_id = extract_video_id(video_url)
        
        if not video_id:
            return None, "Invalid YouTube URL"
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        return transcript_list, None
    
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video"
    except NoTranscriptFound:
        return None, "No transcript found for this video"
    except Exception as e:
        return None, f"Error extracting transcript: {str(e)}"


def detect_topic_changes(transcript_segments, window_size=5, threshold=0.3):
    """
    Detect topic changes in transcript using sliding window similarity
    Returns list of segment indices where topics change
    """
    if len(transcript_segments) < window_size * 2:
        return []
    
    # Combine text from segments
    texts = [seg['text'] for seg in transcript_segments]
    
    # Create sliding windows
    topic_changes = []
    
    for i in range(window_size, len(texts) - window_size):
        # Get text before and after current point
        before_text = ' '.join(texts[i-window_size:i])
        after_text = ' '.join(texts[i:i+window_size])
        
        # Calculate similarity using TF-IDF
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
            tfidf_matrix = vectorizer.fit_transform([before_text, after_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # If similarity is low, it indicates topic change
            if similarity < threshold:
                topic_changes.append(i)
        except:
            continue
    
    # Remove topic changes that are too close to each other
    filtered_changes = []
    last_change = -window_size * 2
    
    for change in topic_changes:
        if change - last_change >= window_size:
            filtered_changes.append(change)
            last_change = change
    
    return filtered_changes


def format_timestamp(seconds):
    """Convert seconds to MM:SS or HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def create_segments_with_topics(transcript_segments, topic_change_indices):
    """
    Create text segments based on topic changes
    Returns list of segments with timestamps and text
    """
    segments = []
    
    # Add first segment
    start_idx = 0
    
    for change_idx in topic_change_indices + [len(transcript_segments)]:
        # Combine text for this segment
        segment_text = ' '.join([seg['text'] for seg in transcript_segments[start_idx:change_idx]])
        start_time = transcript_segments[start_idx]['start']
        
        if segment_text.strip():
            segments.append({
                'timestamp': format_timestamp(start_time),
                'start_seconds': start_time,
                'text': segment_text.strip()
            })
        
        start_idx = change_idx
    
    return segments


def summarize_segment(text, max_sentences=2):
    """Summarize a text segment to key sentences"""
    sentences = sent_tokenize(text)
    
    if len(sentences) <= max_sentences:
        return text
    
    # Simple extractive summarization using sentence position and length
    stop_words = set(stopwords.words('english'))
    
    # Score sentences
    scores = []
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence.lower())
        words = [w for w in words if w.isalnum() and w not in stop_words]
        
        # Score based on position (first sentences are important) and word count
        position_score = 1.0 / (i + 1)
        length_score = min(len(words) / 15, 1.0)  # Normalize to 15 words
        
        scores.append(position_score * 0.6 + length_score * 0.4)
    
    # Get top sentences
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:max_sentences]
    top_indices.sort()  # Maintain original order
    
    summary = ' '.join([sentences[i] for i in top_indices])
    return summary


def summarize_video_with_timestamps(video_url):
    """
    Main function to summarize video with topic changes and timestamps
    """
    # Get transcript
    transcript, error = get_youtube_transcript(video_url)
    
    if error:
        return None, error
    
    if not transcript or len(transcript) == 0:
        return None, "Empty transcript"
    
    # Detect topic changes
    topic_changes = detect_topic_changes(transcript, window_size=5, threshold=0.35)
    
    # Create segments
    segments = create_segments_with_topics(transcript, topic_changes)
    
    # Summarize each segment
    summarized_segments = []
    for segment in segments:
        summary = summarize_segment(segment['text'], max_sentences=2)
        summarized_segments.append({
            'timestamp': segment['timestamp'],
            'summary': summary
        })
    
    # Create full summary
    full_text = ' '.join([seg['text'] for seg in segments])
    
    # Overall statistics
    total_duration = transcript[-1]['start'] + transcript[-1].get('duration', 0)
    
    result = {
        'video_url': video_url,
        'total_duration': format_timestamp(total_duration),
        'total_segments': len(summarized_segments),
        'segments': summarized_segments,
        'full_summary': ' '.join([seg['summary'] for seg in summarized_segments])
    }
    
    return result, None


# Test function
if __name__ == "__main__":
    # Test with a sample YouTube URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result, error = summarize_video_with_timestamps(test_url)
    
    if error:
        print(f"Error: {error}")
    else:
        print("Video Summary:")
        print(f"Duration: {result['total_duration']}")
        print(f"Segments: {result['total_segments']}\n")
        
        for segment in result['segments']:
            print(f"[{segment['timestamp']}] {segment['summary']}\n")
