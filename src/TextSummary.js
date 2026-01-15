import React, { useState } from 'react';
import './TextSummary.css';
import {
  validateText,
  validateFile,
  validateSummarizationMethod,
  validateMaxSentences,
  displayErrors,
  sanitizeText,
  VALIDATION_CONSTANTS
} from './utils/inputValidation';

const TextSummary = () => {
  const [inputText, setInputText] = useState('');
  const [summarizedText, setSummarizedText] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [method, setMethod] = useState('textrank');
  const [maxSentences, setMaxSentences] = useState('auto');
  const [useAutoLength, setUseAutoLength] = useState(true);
  const [validationError, setValidationError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    
    if (!selectedFile) {
      return;
    }
    
    // Validate file
    const validation = validateFile(selectedFile);
    
    if (!validation.isValid) {
      displayErrors(validation.errors);
      setValidationError(validation.errors.join(', '));
      e.target.value = null; // Clear file input
      return;
    }
    
    setFile(selectedFile);
    setInputText(''); // Clear text input when file is selected
    setValidationError('');
  };

  const handleTextChange = (e) => {
    const text = e.target.value;
    
    // Allow typing but show warning if too long
    if (text.length > VALIDATION_CONSTANTS.MAX_TEXT_LENGTH) {
      setValidationError(`Text exceeds maximum length of ${VALIDATION_CONSTANTS.MAX_TEXT_LENGTH} characters`);
    } else {
      setValidationError('');
    }
    
    setInputText(text);
  };

  const handleSummarizeText = async () => {
    // Clear previous errors
    setValidationError('');
    
    // Validate input
    if (!inputText.trim() && !file) {
      displayErrors(['Please enter some text or upload a file to summarize']);
      setValidationError('No input provided');
      return;
    }

    // Validate text if provided
    if (inputText.trim() && !file) {
      const textValidation = validateText(inputText);
      if (!textValidation.isValid) {
        displayErrors(textValidation.errors);
        setValidationError(textValidation.errors.join(', '));
        return;
      }
    }
    
    // Validate file if provided
    if (file) {
      const fileValidation = validateFile(file);
      if (!fileValidation.isValid) {
        displayErrors(fileValidation.errors);
        setValidationError(fileValidation.errors.join(', '));
        return;
      }
    }
    
    // Validate method
    const methodValidation = validateSummarizationMethod(method);
    if (!methodValidation.isValid) {
      displayErrors(methodValidation.errors);
      setValidationError(methodValidation.errors.join(', '));
      return;
    }
    
    // Validate max sentences
    const sentencesValidation = validateMaxSentences(maxSentences);
    if (!sentencesValidation.isValid) {
      displayErrors(sentencesValidation.errors);
      setValidationError(sentencesValidation.errors.join(', '));
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
        formData.append('method', method);
        formData.append('max_sentences', useAutoLength ? 'auto' : maxSentences);
      }
      
      // Create request body for text
      const requestBody = {
        method: method,
        max_sentences: useAutoLength ? 'auto' : parseInt(maxSentences)
      };
      
      if (inputText.trim()) {
        // Sanitize text before sending
        const sanitized = sanitizeText(inputText);
        requestBody.text = sanitized;
      }

      // Send request to backend
      const response = await fetch('http://localhost:5000/api/summarize', {
        method: 'POST',
        headers: file ? {} : { 'Content-Type': 'application/json' },
        body: file ? formData : JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Summarization failed');
      }

      const data = await response.json();
      setSummarizedText(data.summary);
      setStats({
        original: data.original_words,
        summary: data.summary_words,
        compression: data.compression_ratio
      });
    } catch (error) {
      const errorMessage = 'Error: ' + error.message + '\n\nMake sure the backend server is running on port 5000.';
      alert(errorMessage);
      setValidationError(error.message);
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
    setValidationError('');
    const fileInput = document.getElementById('file-input');
    if (fileInput) {
      fileInput.value = null;
    }
  };

  // Calculate character count
  const charCount = inputText.length;
  const isTextTooLong = charCount > VALIDATION_CONSTANTS.MAX_TEXT_LENGTH;
  const isTextTooShort = charCount > 0 && charCount < VALIDATION_CONSTANTS.MIN_TEXT_LENGTH;

  return (
    <div className="text-summary-container">
      <div className="text-summary-box">
        <h2 className="text-summary-title">Text Summarization</h2>
        
        <div className="input-section">
          <div className="file-upload-section">
            <label htmlFor="file-input" className="file-label">
              📁 Upload PDF or TXT file (Max {VALIDATION_CONSTANTS.MAX_FILE_SIZE / (1024 * 1024)}MB):
            </label>
            <input
              id="file-input"
              type="file"
              accept=".pdf,.txt"
              onChange={handleFileChange}
              className="file-input"
            />
            {file && <p className="file-name">✅ Selected: {file.name} ({(file.size / 1024).toFixed(2)} KB)</p>}
          </div>

          <div className="divider">OR</div>

          <div className="textarea-wrapper">
            <textarea
              className={`input-text ${isTextTooLong ? 'error' : ''} ${isTextTooShort ? 'warning' : ''}`}
              placeholder={`Enter or paste your text here (${VALIDATION_CONSTANTS.MIN_TEXT_LENGTH}-${VALIDATION_CONSTANTS.MAX_TEXT_LENGTH} characters)...`}
              value={inputText}
              onChange={handleTextChange}
              disabled={file !== null}
            />
            <div className={`char-count ${isTextTooLong ? 'error' : ''} ${isTextTooShort ? 'warning' : ''}`}>
              {charCount} / {VALIDATION_CONSTANTS.MAX_TEXT_LENGTH} characters
              {isTextTooShort && charCount > 0 && ` (minimum ${VALIDATION_CONSTANTS.MIN_TEXT_LENGTH})`}
            </div>
          </div>

          <div className="options-section">
            <div className="option-group">
              <label>Summarization Method:</label>
              <select value={method} onChange={(e) => setMethod(e.target.value)}>
                <option value="textrank">TextRank (Fast)</option>
                <option value="transformer">AI Model (Better Quality)</option>
              </select>
            </div>

            <div className="option-group">
              <label>Summary Length:</label>
              <select 
                value={useAutoLength ? 'auto' : 'manual'} 
                onChange={(e) => {
                  const isAuto = e.target.value === 'auto';
                  setUseAutoLength(isAuto);
                  if (!isAuto && maxSentences === 'auto') {
                    setMaxSentences(5);
                  }
                }}
              >
                <option value="auto">🤖 Auto (Smart Detection)</option>
                <option value="manual">✍️ Manual (Choose Number)</option>
              </select>
            </div>

            {!useAutoLength && (
              <div className="option-group">
                <label>Number of Sentences (1-20):</label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={maxSentences === 'auto' ? 5 : maxSentences}
                  onChange={(e) => {
                    const val = parseInt(e.target.value);
                    if (val >= 1 && val <= 20) {
                      setMaxSentences(val);
                    }
                  }}
                />
              </div>
            )}
          </div>

          {validationError && (
            <div className="validation-error">
              ⚠️ {validationError}
            </div>
          )}

          <div className="button-group">
            <button 
              className="summarize-button" 
              onClick={handleSummarizeText}
              disabled={loading || isTextTooLong || (charCount > 0 && isTextTooShort && !file)}
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
