# 🎬 Video Summarization Feature Guide

## Overview
The video summarization feature extracts transcripts from YouTube videos, identifies topic changes, and generates timestamped summaries.

## Features

### ✨ Key Capabilities
1. **YouTube Transcript Extraction** - Automatically extracts video captions/subtitles
2. **Topic Change Detection** - Uses AI to identify when topics shift in the video
3. **Timestamped Summaries** - Each topic segment includes a clickable timestamp
4. **Interactive Timeline** - Click timestamps to jump directly to that point in the video
5. **Complete Summary** - Full overview of the entire video content

### 🎯 How It Works

#### Backend Algorithm
1. **Extract Transcript**: Downloads YouTube video transcript with timestamps
2. **Sliding Window Analysis**: Uses a 5-segment window to compare text similarity
3. **Topic Detection**: Calculates TF-IDF cosine similarity between adjacent windows
4. **Segment Creation**: Groups transcript by detected topic changes
5. **Summarization**: Extracts key sentences from each segment using:
   - Position scoring (first sentences weighted higher)
   - Length normalization
   - Stopword filtering

#### Frontend Interface
- Simple URL input for YouTube videos
- Real-time processing status
- Segmented display with timestamps
- Click-to-jump functionality
- Full summary section

## Usage

### Step 1: Enter YouTube URL
```
https://www.youtube.com/watch?v=VIDEO_ID
or
https://youtu.be/VIDEO_ID
```

### Step 2: Click "Summarize Video"
The backend will:
- Extract the video transcript
- Detect topic changes
- Generate summaries for each segment

### Step 3: Review Results
You'll see:
- **Video Info**: Total duration and number of topic segments
- **Timestamped Segments**: Each topic with its timestamp
- **Full Summary**: Complete overview of the video

### Step 4: Interactive Navigation
Click any timestamp button to:
- Open YouTube video at that exact moment
- New tab opens automatically

## Technical Details

### Backend API Endpoint
```
POST /api/summarize/video
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### Response Format
```json
{
  "success": true,
  "video_url": "...",
  "total_duration": "HH:MM:SS",
  "total_segments": 5,
  "segments": [
    {
      "timestamp": "00:00",
      "summary": "Introduction to the topic..."
    },
    {
      "timestamp": "02:15",
      "summary": "Detailed explanation of..."
    }
  ],
  "full_summary": "Complete summary text..."
}
```

### Algorithm Parameters
- **Window Size**: 5 segments (adjustable in `video_summarizer_api.py`)
- **Similarity Threshold**: 0.35 (lower = more topic changes detected)
- **Sentences per Segment**: 2 (for concise summaries)
- **Min Window Distance**: 5 segments between topic changes

## Requirements

### Python Packages
```bash
pip install youtube-transcript-api==0.6.1
```

Already included:
- `nltk` - Text processing
- `scikit-learn` - TF-IDF and similarity calculations
- `numpy` - Numerical operations

### Important Notes
1. **Captions Required**: Video must have captions/subtitles enabled
2. **Language**: Currently supports English transcripts
3. **Public Videos**: Video must be publicly accessible
4. **Backend**: Must be running on port 5000

## Troubleshooting

### "Transcripts are disabled for this video"
- Video doesn't have captions/subtitles enabled
- Try another video with auto-generated or manual captions

### "No transcript found"
- Captions may not be available in English
- Video may be private or restricted

### "Invalid YouTube URL"
- Ensure URL format is correct
- Must be a YouTube link (youtube.com or youtu.be)

### Backend Connection Error
- Verify backend is running: `python backend_api.py`
- Check port 5000 is not blocked
- Ensure `youtube-transcript-api` is installed

## Future Enhancements
- [ ] Multi-language support
- [ ] Custom similarity thresholds
- [ ] Video download option
- [ ] Export summaries to PDF/TXT
- [ ] Playlist support
- [ ] Keyword extraction
- [ ] Sentiment analysis per segment

## Examples

### Good Videos to Test
Videos with clear topic transitions work best:
- Educational lectures
- Tutorial videos
- Documentary series
- Podcast recordings
- Conference talks

### Example Output
```
[00:00] Introduction to machine learning concepts and basic terminology.
[02:45] Deep dive into neural networks architecture and components.
[05:30] Practical applications of machine learning in real-world scenarios.
[08:15] Future trends and emerging technologies in AI development.
```

## Credits
- **YouTube Transcript API**: For transcript extraction
- **NLTK**: Natural language processing
- **Scikit-learn**: Machine learning utilities
- **Flask**: Backend API framework
- **React**: Frontend interface

---

## Quick Start Commands

### Install Dependencies
```bash
cd ai-text-and-video-summarizer-main
pip install -r requirements.txt
```

### Start Backend
```bash
python backend_api.py
```

### Start Frontend
```bash
npm start
```

### Test Video Summarization
1. Navigate to "Video Summary" page
2. Paste any YouTube URL with captions
3. Click "Summarize Video"
4. Click timestamps to jump to that point

---

**Enjoy exploring video content more efficiently! 🚀**
