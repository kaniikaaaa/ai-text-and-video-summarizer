import React, { useState } from 'react';
import './TextSummary.css';

const TextSummary = () => {
  const [inputText, setInputText] = useState('');
  const [summarizedText, setSummarizedText] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [method, setMethod] = useState('textrank');
  const [maxSentences, setMaxSentences] = useState(5);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const fileType = selectedFile.name.split('.').pop().toLowerCase();
      if (fileType === 'pdf' || fileType === 'txt') {
        setFile(selectedFile);
        setInputText(''); // Clear text input when file is selected
      } else {
        alert('Please upload a PDF or TXT file only.');
        e.target.value = null;
      }
    }
  };

  const handleSummarizeText = async () => {
    if (!inputText.trim() && !file) {
      alert('Please enter some text or upload a file to summarize.');
      return;
    }

    setLoading(true);
    setSummarizedText('');
    setStats(null);

    try {
      const formData = new FormData();
      
      if (file) {
        // If file is uploaded, send the file
        formData.append('file', file);
      }
      
      // Create request body for text or additional parameters
      const requestBody = {
        method: method,
        max_sentences: maxSentences
      };
      
      if (inputText.trim()) {
        requestBody.text = inputText;
      }

      // Send request to backend
      const response = await fetch('http://localhost:5000/api/summarize', {
        method: 'POST',
        headers: file ? {} : { 'Content-Type': 'application/json' },
        body: file ? (() => {
          formData.append('method', method);
          formData.append('max_sentences', maxSentences);
          return formData;
        })() : JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Summarization failed');
      }

      const data = await response.json();
      setSummarizedText(data.summary);
      setStats({
        original: data.original_word_count,
        summary: data.summary_word_count,
        compression: data.compression_ratio
      });
    } catch (error) {
      alert('Error: ' + error.message + '\n\nMake sure the backend server is running on port 5000.');
      console.error('Summarization error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setFile(null);
    setSummarizedText('');
    setStats(null);
    document.getElementById('file-input').value = null;
  };

  return (
    <div className="text-summary-container">
      <div className="text-summary-box">
        <h2 className="text-summary-title">Text Summarization</h2>
        
        <div className="input-section">
          <div className="file-upload-section">
            <label htmlFor="file-input" className="file-label">
              📁 Upload PDF or TXT file:
            </label>
            <input
              id="file-input"
              type="file"
              accept=".pdf,.txt"
              onChange={handleFileChange}
              className="file-input"
            />
            {file && <p className="file-name">Selected: {file.name}</p>}
          </div>

          <div className="divider">OR</div>

          <textarea
            className="input-text"
            placeholder="Enter or paste your text here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={file !== null}
          />

          <div className="options-section">
            <div className="option-group">
              <label>Summarization Method:</label>
              <select value={method} onChange={(e) => setMethod(e.target.value)}>
                <option value="textrank">TextRank (Fast)</option>
                <option value="transformer">AI Model (Better Quality)</option>
              </select>
            </div>

            <div className="option-group">
              <label>Max Sentences:</label>
              <input
                type="number"
                min="1"
                max="20"
                value={maxSentences}
                onChange={(e) => setMaxSentences(parseInt(e.target.value))}
              />
            </div>
          </div>

          <div className="button-group">
            <button 
              className="summarize-button" 
              onClick={handleSummarizeText}
              disabled={loading}
            >
              {loading ? '⏳ Summarizing...' : '✨ Summarize'}
            </button>
            <button className="clear-button" onClick={handleClear}>
              🗑️ Clear
            </button>
          </div>
        </div>

        {stats && (
          <div className="stats-box">
            <p>📊 Original: {stats.original} words | Summary: {stats.summary} words | Compression: {stats.compression}%</p>
          </div>
        )}

        {summarizedText && (
          <div className="summary-box">
            <h3 className="summary-title">📝 Summarized Text:</h3>
            <p className="summary-text">{summarizedText}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TextSummary;
