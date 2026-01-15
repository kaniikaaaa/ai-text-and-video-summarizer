#!/usr/bin/env python3
"""Quick test script to debug YouTube transcript extraction"""

from youtube_transcript_api import YouTubeTranscriptApi
import traceback

# Test different video URLs
test_urls = [
    "https://youtu.be/PGUdWfB8nLg?si=-WU5_CHztdMGl9P6",
    "https://www.youtube.com/watch?v=8pTEmbeENF4",  # Known working video
    "https://www.youtube.com/watch?v=yJg-Y5byMMw",  # TED-Ed video
]

def extract_video_id(url):
    """Extract video ID from URL"""
    import re
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

for url in test_urls:
    print(f"\n{'='*60}")
    print(f"Testing URL: {url}")
    print('='*60)
    
    try:
        video_id = extract_video_id(url)
        print(f"Video ID: {video_id}")
        
        if not video_id:
            print("❌ Could not extract video ID")
            continue
        
        # Try to get transcript
        print("Attempting to fetch transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        print(f"✅ SUCCESS! Got {len(transcript)} segments")
        print(f"First segment: {transcript[0]}")
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()

print("\n" + "="*60)
print("Test complete!")
