import React, { useState } from 'react';
import './VideoSummary.css';
import {
  validateYouTubeURL,
  displayErrors
} from './utils/inputValidation';

function VideoSummary() {
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [validationError, setValidationError] = useState('');

  const handleSummarizeVideo = async () => {
    // Clear previous errors
    setError('');
    setValidationError('');
    
    // Validate YouTube URL
    const validation = validateYouTubeURL(videoUrl);
    
    if (!validation.isValid) {
      displayErrors(validation.errors);
      setValidationError(validation.errors.join(', '));
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      // Use sanitized URL from validation
      const response = await fetch('http://localhost:5000/api/summarize/video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: validation.sanitized
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to summarize video');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred while summarizing the video');
      console.error('Video summarization error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setVideoUrl('');
    setResult(null);
    setError('');
    setValidationError('');
  };
  
  // Handle URL input change with basic validation
  const handleUrlChange = (e) => {
    const url = e.target.value;
    setVideoUrl(url);
    
    // Clear validation error when user starts typing
    if (validationError) {
      setValidationError('');
    }
  };

  const handleTimestampClick = (timestamp) => {
    // Extract video ID and create timestamped URL
    const videoId = extractVideoId(videoUrl);
    if (videoId) {
      const timeInSeconds = convertTimestampToSeconds(timestamp);
      const timestampedUrl = `https://www.youtube.com/watch?v=${videoId}&t=${timeInSeconds}s`;
      window.open(timestampedUrl, '_blank');
    }
  };

  const extractVideoId = (url) => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/,
      /youtube\.com\/embed\/([^&\n?#]+)/,
      /youtube\.com\/v\/([^&\n?#]+)/
    ];
    
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return null;
  };

  const convertTimestampToSeconds = (timestamp) => {
    const parts = timestamp.split(':').map(Number);
    if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2];
    } else if (parts.length === 2) {
      return parts[0] * 60 + parts[1];
    }
    return 0;
  };

  return (
    <div className="video-summary-container">
      <div className="video-summary-box">
        <h2 className="video-summary-title">📹 Video Summarization</h2>
        
        <div className="video-input-section">
          <label htmlFor="video-url" className="video-label">
            YouTube Video URL:
          </label>
          <input
            id="video-url"
            type="text"
            className={`input-url ${validationError ? 'error' : ''}`}
            placeholder="https://youtube.com/watch?v=... or https://youtu.be/..."
            value={videoUrl}
            onChange={handleUrlChange}
          />
          
          {validationError && (
            <div className="validation-error">
              ⚠️ {validationError}
            </div>
          )}

          <div className="button-group">
            <button 
              className="summarize-video-button" 
              onClick={handleSummarizeVideo}
              disabled={loading || !videoUrl.trim()}
            >
              {loading ? '⏳ Processing...' : '🎬 Summarize Video'}
            </button>
            <button className="clear-button" onClick={handleClear}>
              🗑️ Clear
            </button>
          </div>
        </div>

        {error && (
          <div className="error-box">
            <p className="error-text">❌ {error}</p>
            <p className="error-hint">
              Make sure:
              • The backend server is running on port 5000
              <br />
              • The video has captions/subtitles available
              <br />
              • The URL is a valid YouTube link
            </p>
          </div>
        )}

        {result && (
          <div className="video-result">
            <div className="video-info-box">
              <p className="video-info">
                📊 Duration: <strong>{result.total_duration}</strong> | 
                Segments: <strong>{result.total_segments}</strong> topic changes detected
              </p>
            </div>

            <div className="segments-container">
              <h3 className="segments-title">⏱️ Summary with Timestamps</h3>
              <p className="segments-hint">Click on timestamps to jump to that point in the video</p>
              
              {result.segments.map((segment, index) => (
                <div key={index} className="segment-card">
                  <button 
                    className="timestamp-button"
                    onClick={() => handleTimestampClick(segment.timestamp)}
                    title="Click to jump to this timestamp"
                  >
                    🕒 {segment.timestamp}
                  </button>
                  <p className="segment-text">{segment.summary}</p>
                </div>
              ))}
            </div>

            <div className="full-summary-box">
              <h3 className="full-summary-title">📝 Complete Summary</h3>
              <p className="full-summary-text">{result.full_summary}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default VideoSummary;
