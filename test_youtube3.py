#!/usr/bin/env python3
"""Testing correct YouTube Transcript API v1.2.3 syntax"""

from youtube_transcript_api import YouTubeTranscriptApi

video_ids = [
    "8pTEmbeENF4",  # Known working video
    "PGUdWfB8nLg",  # User's video
]

for video_id in video_ids:
    print(f"\nTesting video: {video_id}")
    print("="*50)
    
    try:
        # Try new API syntax
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id)
        print(f"SUCCESS! Got transcript")
        print(f"Type: {type(result)}")
        if isinstance(result, list) and len(result) > 0:
            print(f"First entry: {result[0]}")
        else:
            print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
