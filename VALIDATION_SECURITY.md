# 🛡️ Input Validation & Security Documentation

## Overview
Comprehensive input validation and sanitization implemented across both frontend and backend to ensure security and data integrity.

---

## 🎯 Features Implemented

### 1. **Frontend Validation** (React)
- Real-time input validation
- User-friendly error messages
- Visual feedback (color-coded inputs)
- Character count display
- File type and size validation

### 2. **Backend Validation** (Python/Flask)
- Server-side validation (cannot be bypassed)
- Sanitization of all inputs
- Rate limiting per IP address
- Malicious content detection
- XSS prevention

---

## 📝 Text Summarization Validation

### Frontend (`TextSummary.js`)

#### Text Input Validation:
- ✅ **Minimum Length**: 50 characters
- ✅ **Maximum Length**: 50,000 characters (50KB)
- ✅ **Character Counter**: Real-time display
- ✅ **Sanitization**: Removes null bytes, control characters
- ✅ **XSS Detection**: Checks for `<script>`, `<iframe>`, `javascript:`, event handlers

```javascript
// Example validation
const validation = validateText(inputText);
if (!validation.isValid) {
  // Show error to user
  displayErrors(validation.errors);
}
```

#### File Upload Validation:
- ✅ **Allowed Types**: PDF, TXT only
- ✅ **Maximum Size**: 10MB
- ✅ **Filename Security**: Prevents directory traversal (`..`), invalid characters
- ✅ **Empty File Check**: Rejects zero-byte files

```javascript
const validation = validateFile(selectedFile);
// Returns: { isValid, errors, fileType, fileSize, fileName }
```

#### Method Validation:
- ✅ **Allowed Methods**: `textrank`, `transformer`
- ✅ **Default**: `textrank` if invalid

#### Sentences Validation:
- ✅ **Range**: 1-20 sentences or 'auto'
- ✅ **Type Check**: Must be integer or string 'auto'

---

## 🎬 Video Summarization Validation

### Frontend (`VideoSummary.js`)

#### URL Validation:
- ✅ **Empty Check**: Cannot be blank
- ✅ **Length Limit**: Max 2048 characters
- ✅ **Protocol Check**: Only HTTP/HTTPS allowed
- ✅ **Domain Verification**: Must be YouTube
  - `youtube.com`
  - `www.youtube.com`
  - `m.youtube.com`
  - `youtu.be`
- ✅ **Video ID Extraction**: 11-character alphanumeric format
- ✅ **URL Sanitization**: Removes whitespace

```javascript
const validation = validateYouTubeURL(videoUrl);
// Returns: { isValid, errors, sanitized, videoId }
```

---

## 🔐 Backend Security

### Backend Validation (`backend_validation.py`)

#### 1. Text Sanitization
```python
def sanitize_text(text):
    # Remove null bytes
    # Remove control characters
    # Normalize whitespace
    # Trim
    return sanitized_text
```

#### 2. Malicious Content Detection
Checks for:
- `<script>` tags
- `<iframe>` tags
- `javascript:` protocol
- Event handlers (`onclick=`, `onerror=`, etc.)

#### 3. Rate Limiting
```python
# Limits per IP address
- Text Summarization: 50 requests/minute
- Video Summarization: 20 requests/minute
```

#### 4. File Validation
- Extension whitelist
- Size limits enforced
- Filename security checks

---

## 🎨 User Interface Feedback

### Visual Indicators

#### Text Input States:
```css
/* Normal */
.input-text { border: 2px solid #cccccc; }

/* Warning (too short) */
.input-text.warning { 
  border-color: #f57c00; 
  background-color: #fff3e0; 
}

/* Error (too long) */
.input-text.error { 
  border-color: #d32f2f; 
  background-color: #ffebee; 
}
```

#### Character Counter:
- Gray: Normal
- Orange: Warning (< 50 chars)
- Red: Error (> 50,000 chars)

#### Validation Errors:
```jsx
<div className="validation-error">
  ⚠️ {errorMessage}
</div>
```

---

## 🧪 Testing Examples

### Valid Inputs

#### Text:
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit... 
(minimum 50 characters)
```

#### YouTube URLs:
```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://youtube.com/watch?v=VIDEO_ID
```

### Invalid Inputs (Will be Rejected)

#### Text:
```
❌ "Short text" (< 50 chars)
❌ Empty string
❌ Text with <script>alert('xss')</script>
❌ Text > 50,000 characters
```

#### Files:
```
❌ file.exe (wrong type)
❌ file.docx (wrong type)
❌ 15MB file (too large)
❌ Empty file (0 bytes)
❌ Filename with "../../../etc/passwd"
```

#### URLs:
```
❌ "not a url"
❌ "ftp://youtube.com/video"
❌ "https://vimeo.com/video"
❌ "https://youtube.com" (no video ID)
```

---

## 🚀 Implementation Files

### Frontend:
1. `src/utils/inputValidation.js` - Validation utilities
2. `src/TextSummary.js` - Text page with validation
3. `src/VideoSummary.js` - Video page with validation
4. `src/TextSummary.css` - Validation styles
5. `src/VideoSummary.css` - Validation styles

### Backend:
1. `backend_validation.py` - Server-side validation
2. `backend_api.py` - API endpoints with validation

---

## 📊 Security Benefits

### Protection Against:
✅ **XSS (Cross-Site Scripting)** - HTML/JS injection prevented
✅ **Path Traversal** - Directory navigation blocked
✅ **DoS (Denial of Service)** - Rate limiting implemented
✅ **Code Injection** - Input sanitization
✅ **Buffer Overflow** - Length limits enforced
✅ **Malformed Data** - Type checking and validation

### Best Practices Followed:
✅ **Defense in Depth** - Multiple validation layers
✅ **Fail Secure** - Defaults to safe state
✅ **Input Validation** - Whitelist approach
✅ **Output Encoding** - Sanitized before use
✅ **Least Privilege** - Minimal permissions

---

## 🔄 Validation Flow

```
User Input → Frontend Validation → Sanitization → Backend Validation → Processing
     ↓              ↓                    ↓               ↓              ↓
   Input        UI Feedback         Clean Data    Security Check    Safe Result
```

---

## ⚙️ Configuration

### Adjustable Limits

#### `inputValidation.js` (Frontend):
```javascript
const MAX_TEXT_LENGTH = 50000;
const MIN_TEXT_LENGTH = 50;
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
```

#### `backend_validation.py` (Backend):
```python
MAX_TEXT_LENGTH = 50000
MIN_TEXT_LENGTH = 50
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

#### Rate Limits (`backend_api.py`):
```python
# Text endpoint
check_rate_limit(ip, limit=50, window=60)  # 50/min

# Video endpoint  
check_rate_limit(ip, limit=20, window=60)  # 20/min
```

---

## 📝 Error Messages

### User-Friendly Messages:
- ❌ "Text must be at least 50 characters"
- ❌ "File size exceeds 10MB limit"
- ❌ "Invalid file type. Only PDF and TXT files are allowed"
- ❌ "URL must be a valid YouTube link"
- ❌ "Rate limit exceeded. Max 50 requests per 60 seconds"

---

## 🎓 Usage Examples

### Frontend Validation:
```javascript
import { validateText, displayErrors } from './utils/inputValidation';

const validation = validateText(inputText);
if (!validation.isValid) {
  displayErrors(validation.errors);
  setValidationError(validation.errors.join(', '));
  return;
}

// Use sanitized text
const cleanText = validation.sanitized;
```

### Backend Validation:
```python
from backend_validation import validate_text, validate_youtube_url

# Text validation
is_valid, errors, sanitized = validate_text(text)
if not is_valid:
    return jsonify({'error': '; '.join(errors)}), 400

# URL validation
is_valid, errors, sanitized, video_id = validate_youtube_url(url)
if not is_valid:
    return jsonify({'error': '; '.join(errors)}), 400
```

---

## 🔍 Monitoring & Logging

### Backend Logs:
```python
app.logger.error(f"Text validation failed: {errors}")
app.logger.warning(f"Rate limit exceeded for {client_ip}")
app.logger.info(f"Processing video URL: {sanitized_url}")
```

---

## ✅ Testing Checklist

- [x] Empty input validation
- [x] Minimum length validation
- [x] Maximum length validation
- [x] File type validation
- [x] File size validation
- [x] URL format validation
- [x] XSS prevention
- [x] Path traversal prevention
- [x] Rate limiting
- [x] Sanitization
- [x] Error handling
- [x] UI feedback

---

## 🎉 Summary

**Comprehensive security implementation** with:
- ✅ 15+ validation checks
- ✅ Real-time user feedback
- ✅ Server-side enforcement
- ✅ Rate limiting
- ✅ XSS prevention
- ✅ Beautiful UI integration

**Your application is now production-ready and secure!** 🛡️🚀

