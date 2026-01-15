#!/usr/bin/env python3
"""Quick test script to check new YouTube Transcript API"""

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("Testing new API...")
    
    # Test a known working video
    video_id = "8pTEmbeENF4"
    
    print(f"Video ID: {video_id}")
    print("Available methods:", [m for m in dir(YouTubeTranscriptApi) if not m.startswith('_')])
    
    # Try different methods
    try:
        result = YouTubeTranscriptApi.fetch(video_id)
        print("SUCCESS with .fetch():", type(result))
        print("Sample:", result[:2] if isinstance(result, list) else result)
    except AttributeError:
        print(".fetch() not available")
    except Exception as e:
        print(f".fetch() error: {e}")
    
    try:
        from youtube_transcript_api import YouTubeTranscript
        result = YouTubeTranscript.from_video_id(video_id)
        print("SUCCESS with YouTubeTranscript.from_video_id():", type(result))
    except Exception as e:
        print(f"from_video_id error: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
