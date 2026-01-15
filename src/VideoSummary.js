import React, { useState } from 'react';
import './VideoSummary.css';

function VideoSummary() {
  const [videoUrl, setVideoUrl] = useState('');
  const [summarizedText, setSummarizedText] = useState('');

  const handleSummarizeVideo = () => {
    if (!videoUrl) {
      alert('Please enter a video URL to summarize.');
      return;
    }

    // Simulating a video summarization process
    setSummarizedText(
      "This is a placeholder summary for the video at the provided URL. A real summarization algorithm would process the video's audio and generate a summary."
    );
  };

  return (
    <div className="video-summary-container">
      <div className="video-summary-box">
        <h2>Video Summarization</h2>
        <input
          type="text"
          className="video-url-input"
          placeholder="Enter video URL here"
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
        />
        <button className="summarize-button" onClick={handleSummarizeVideo}>
          Summarize Video
        </button>
        {summarizedText && (
          <div className="summary-box">
            <h3>Summarized Text:</h3>
            <p>{summarizedText}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default VideoSummary;

