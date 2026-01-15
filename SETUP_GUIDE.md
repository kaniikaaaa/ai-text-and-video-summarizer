# AI Text & Video Summarizer - Setup Guide

## 🚀 Features
- ✨ **Text Summarization** with AI-powered algorithms
- 📄 **PDF Upload Support** - Upload and summarize PDF documents
- 📝 **Text File Support** - Upload .txt files
- 🎯 **Multiple Algorithms**:
  - TextRank (Fast, efficient)
  - Transformer AI Model (Better quality, uses BART)
- 📊 **Statistics** - See word count and compression ratio
- 🔒 **Authentication** - Protected routes with login/signup
- 🔐 **Secure Password Hashing** - Using Argon2

## 📋 Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn

## 🛠️ Installation Steps

### Backend Setup (Python/Flask)

1. **Install Python dependencies:**
```bash
cd ai-text-and-video-summarizer-main
pip install -r requirements.txt
```

2. **Download NLTK data (if not auto-downloaded):**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

3. **Start the Flask backend server:**
```bash
python backend_api.py
```
The backend will run on `http://localhost:5000`

### Frontend Setup (React)

1. **Install Node dependencies:**
```bash
npm install
```

2. **Start the React development server:**
```bash
npm start
```
The frontend will run on `http://localhost:3000`

## 📖 How to Use

### Text Summarization

1. **Navigate to Text Summary page** (after login)
2. **Choose input method:**
   - Upload a PDF or TXT file, OR
   - Type/paste text directly
3. **Select options:**
   - **Method**: TextRank (fast) or Transformer (better quality)
   - **Max Sentences**: Number of sentences in summary (1-20)
4. **Click "Summarize"** button
5. **View results:**
   - Original and summary word counts
   - Compression ratio
   - Highlighted summary text

### Features Explained

#### TextRank Algorithm
- Fast processing
- Extractive summarization (picks important sentences)
- Works offline
- Good for quick summaries

#### Transformer AI Model
- Uses Facebook's BART model
- Better quality summaries
- More natural language
- Requires more processing power
- First run might take time to download model

## 🔧 API Endpoints

### Health Check
```
GET http://localhost:5000/api/health
```

### Summarize Text
```
POST http://localhost:5000/api/summarize

Body (JSON):
{
  "text": "Your text here...",
  "method": "textrank" or "transformer",
  "max_sentences": 5
}

Or (FormData for file upload):
- file: PDF or TXT file
- method: "textrank" or "transformer"
- max_sentences: number
```

Response:
```json
{
  "original_text": "...",
  "summary": "...",
  "original_word_count": 500,
  "summary_word_count": 100,
  "compression_ratio": 80.0
}
```

## 🔐 Security Features

1. **Password Hashing**: Argon2id algorithm
2. **Protected Routes**: Must login to access summarization pages
3. **SSL**: Enabled for secure connections
4. **CORS**: Configured for frontend-backend communication

## 🐛 Troubleshooting

### Backend not starting?
- Check if Python is installed: `python --version`
- Check if all packages are installed: `pip list`
- Make sure port 5000 is not in use

### Frontend not connecting to backend?
- Ensure backend is running on port 5000
- Check browser console for errors
- Verify CORS is enabled in Flask

### Transformer model not working?
- Check if you have enough RAM (model requires ~1GB)
- System will automatically fallback to TextRank if transformer fails
- Check backend logs for detailed error messages

### NLTK data errors?
```bash
python -c "import nltk; nltk.download('all')"
```

## 📦 File Structure
```
ai-text-and-video-summarizer-main/
├── backend_api.py          # Flask backend API
├── text-summarizer.py      # Standalone Python summarizer
├── feature_text.py         # Feature extraction utilities
├── Login.js                # Login component
├── Signup.js               # Signup component
├── Home.js                 # Home page
├── TextSummary.js          # Text summarization component
├── VideoSummary.js         # Video summarization component
├── AuthContext.js          # Authentication context
├── ProtectedRoute.js       # Route protection
├── App.js                  # Main app component
├── requirements.txt        # Python dependencies
├── package.json            # Node dependencies
└── README.md               # Project documentation
```

## 💡 Tips

1. **For best results**: Use the Transformer model with 3-7 sentences
2. **For speed**: Use TextRank with any sentence count
3. **PDF files**: Make sure they contain extractable text (not scanned images)
4. **Long documents**: May take longer to process with Transformer model
5. **Memory**: Transformer model requires good RAM, consider TextRank for low-end systems

## 🎯 Future Enhancements
- Video summarization integration
- Multiple language support
- Save summaries to database
- Export summaries as PDF
- Batch processing
- User preferences storage

## 📝 Notes
- First time using Transformer model will download ~1.6GB model files
- TextRank is recommended for documents over 5000 words
- Ensure stable internet for initial model downloads

## 🤝 Support
If you encounter any issues, please check:
1. All dependencies are installed
2. Backend server is running
3. Frontend can connect to backend
4. Browser console for detailed errors

Happy Summarizing! ✨
