# Concisely - AI Text and Video Summarizer

An intelligent web application that leverages Natural Language Processing and Deep Learning to generate concise, well-formatted summaries from text documents (including PDFs) and YouTube videos.

## Overview

Concisely is designed to help users quickly extract key information from lengthy content with intelligent formatting, grammar correction, and structure preservation. The application provides comprehensive text and video summarization with automatic length detection and professional output formatting.

## ✨ Features

### Text Summarization
- **PDF & Text Upload**: Support for PDF files, TXT files, and direct text input
- **Dual Summarization Methods**: TextRank (extractive) and Transformer-based (BART) summarization
- **Auto-Length Detection**: Automatically determines optimal summary length based on content
- **Smart Formatting**: Preserves document structure (headings, bullets, sections)
- **Resume Intelligence**: Special handling for resumes with clean contact information extraction
- **Grammar Correction**: 11-step pipeline for polished, professional output
- **Input Validation**: Frontend and backend validation with XSS prevention

### Video Summarization
- **YouTube Integration**: Extract transcripts from YouTube videos
- **Topic Detection**: Automatically detects topic changes using TF-IDF and cosine similarity
- **Timestamped Segments**: Provides timestamps for each topic section
- **Grammar Polish**: Same professional grammar correction as text summaries

### Security & Validation
- **3-Layer Security**: Frontend validation, backend validation, and sanitization
- **Rate Limiting**: Protection against DoS attacks
- **XSS Prevention**: Input sanitization across all endpoints
- **File Validation**: Type and size checks for uploaded files

### User Features
- **Authentication**: Secure signup and login with persistent sessions
- **Remember Me**: Credentials stored with SHA-256 hashing
- **Protected Routes**: Access control for authenticated users
- **Responsive Design**: Modern UI with smooth scrolling
- **Theme Support**: Light/dark theme toggle

## 🛠 Technology Stack

### Frontend
- **React.js** - UI framework
- **React Router** - Navigation and protected routes
- **CSS3** - Modern styling with flexbox
- **localStorage** - Client-side credential storage

### Backend
- **Flask** - Python web framework with CORS support
- **NLTK** - Natural language tokenization and preprocessing
- **Transformers (Hugging Face)** - BART model for abstractive summarization
- **scikit-learn** - TF-IDF vectorization and similarity calculations
- **youtube-transcript-api** - YouTube transcript extraction
- **PyPDF2** - PDF text extraction
- **defusedxml** - Secure XML parsing

### AI/ML Components
- **TextRank Algorithm**: Extractive summarization using eigenvector centrality
- **BART Transformer**: Abstractive summarization with facebook/bart-large-cnn
- **TF-IDF Vectorization**: Topic change detection for video segmentation
- **Cosine Similarity**: Sentence similarity and topic clustering
- **Grammar Correction**: 11-step regex-based post-processing pipeline
- **Smart Formatting**: Document structure detection and preservation

## 📁 Project Structure

```
ai-text-and-video-summarizer/
├── src/                           # React frontend
│   ├── App.js                    # Main app with routing
│   ├── AuthContext.js            # Authentication context
│   ├── ProtectedRoute.js         # Route protection
│   ├── Login.js                  # Login page
│   ├── Signup.js                 # Registration page
│   ├── Home.js                   # Dashboard
│   ├── Landing.js                # Landing page
│   ├── TextSummary.js            # Text summarization UI
│   ├── VideoSummary.js           # Video summarization UI
│   ├── userStorage.js            # User credential management
│   └── utils/
│       └── inputValidation.js    # Frontend validation
├── backend_api.py                # Main Flask API server
├── video_summarizer_api.py       # YouTube video processing
├── grammar_corrector.py          # Grammar correction pipeline
├── smart_formatter.py            # Intelligent document formatting
├── resume_preprocessor.py        # Resume-specific preprocessing
├── backend_validation.py         # Backend input validation
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies
├── database.sql                  # Database schema
├── start_backend.bat             # Windows: Start Flask server
└── start_frontend.bat            # Windows: Start React app
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** v14 or higher
- **Python** 3.8+
- **npm** or yarn package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/kaniikaaaa/ai-text-and-video-summarizer.git
cd ai-text-and-video-summarizer
```

2. **Install frontend dependencies:**
```bash
npm install
```

3. **Install backend dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data:**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

### Running the Application

#### Option 1: Using Batch Files (Windows)
```bash
# Terminal 1: Start backend
start_backend.bat

# Terminal 2: Start frontend
start_frontend.bat
```

#### Option 2: Manual Start
```bash
# Terminal 1: Start Flask backend
python backend_api.py

# Terminal 2: Start React frontend
npm start
```

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

## 📖 How It Works

### Text Summarization Pipeline

1. **Input Validation**: Frontend and backend validation with sanitization
2. **Resume Detection**: Automatically detects if input is a resume
3. **Preprocessing**: Cleans and structures text (especially contact info for resumes)
4. **Summarization**: TextRank or Transformer generates summary with auto-length
5. **Grammar Correction**: 11-step pipeline fixes capitalization, punctuation, grammar
6. **Smart Formatting**: Applies document structure (headings, bullets, sections)
7. **Output**: Clean, professional, well-structured summary

### Video Summarization Pipeline

1. **URL Validation**: Checks for valid YouTube URL format
2. **Transcript Extraction**: Downloads video transcript with timing
3. **Topic Detection**: Uses TF-IDF to identify topic changes
4. **Segmentation**: Groups transcript into coherent topic sections
5. **Summarization**: TextRank on each segment
6. **Grammar Polish**: Professional grammar correction
7. **Output**: Timestamped topic summaries with video duration

### Grammar Correction (11 Steps)

1. Contact info formatting (resume-specific)
2. Contraction expansion
3. Punctuation fixes
4. Sentence structure improvement
5. Capitalization
6. Redundant phrase removal
7. Common grammar mistakes
8. Article usage improvement
9. Final punctuation polish
10. Multiple punctuation removal
11. Consistent spacing

### Smart Formatting

- **Document Type Detection**: Resume, report, article, or general
- **Structure Recognition**: Headings, bullets, sections, paragraphs
- **Contact Extraction**: Email, phone, GitHub, LinkedIn
- **Hierarchy Preservation**: Maintains original document organization
- **Professional Output**: Clean sections with proper spacing

## 🎯 Usage

### Text Summarization

1. Navigate to **Text Summary** page
2. Choose input method:
   - Upload PDF file
   - Upload TXT file
   - Paste/type text directly
3. Select summarization method:
   - **TextRank** (fast, extractive)
   - **Transformer** (advanced, abstractive)
   - **Auto (Smart Detection)** - automatically chooses optimal length
4. Click **Generate Summary**
5. View formatted summary with statistics

### Video Summarization

1. Navigate to **Video Summary** page
2. Paste YouTube URL
3. Click **Summarize Video**
4. View:
   - Video duration
   - Number of segments
   - Timestamped topic summaries

## 🔐 Security Features

- **Input Validation**: Text length, file type/size, URL format
- **XSS Prevention**: HTML entity encoding and dangerous pattern removal
- **Rate Limiting**: 100 requests per minute per IP
- **File Security**: Type whitelist (PDF, TXT) and 10MB size limit
- **Safe Parsing**: defusedxml for XML, secure PDF extraction
- **SHA-256 Hashing**: Client-side password hashing for storage

## 📊 API Endpoints

### POST `/api/summarize`
- **Purpose**: Text/PDF summarization
- **Params**: `text`, `file`, `method`, `max_sentences`
- **Returns**: `summary`, `original_word_count`, `summary_word_count`, `reduction_percentage`

### POST `/api/summarize/video`
- **Purpose**: YouTube video summarization
- **Params**: `video_url`
- **Returns**: `video_duration`, `total_segments`, `timestamped_segments`


## 🧪 Development

### Available Scripts

- `npm start` - Run development server
- `npm build` - Build production application
- `npm test` - Run test suite
- `python backend_api.py` - Start Flask backend with debug mode

### Testing Backend Independently

```python
# Test text summarization
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here...", "method": "textrank", "max_sentences": "auto"}'

# Test video summarization
curl -X POST http://localhost:5000/api/summarize/video \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to your branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🎨 Screenshots

![Landing Page](https://github.com/user-attachments/assets/dea8c750-bc26-4eb5-9027-c12d68ae0649)
![Application Interface](https://github.com/user-attachments/assets/1458ba31-329b-47cc-bf47-0890f382bea8)

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- **NLTK** - Natural language processing toolkit
- **Hugging Face Transformers** - BART summarization model
- **React** - Frontend framework
- **Flask** - Backend framework
- **scikit-learn** - Machine learning utilities
- **youtube-transcript-api** - YouTube transcript extraction

## 📧 Contact

For questions, feedback, or issues, please open an issue on the [GitHub repository](https://github.com/kaniikaaaa/ai-text-and-video-summarizer).

---

**Built with ❤️ using AI, NLP, and modern web technologies**
