# Concisely - AI Text and Video Summarizer

An intelligent web application that leverages Natural Language Processing and Deep Learning to generate concise summaries from text documents and video content.

## Overview

Concisely is designed to help users quickly extract key information from lengthy content. The application provides two core functionalities: text summarization using extractive summarization techniques and video summarization capabilities.

## Features

- **Text Summarization**: Extract key sentences from long articles, documents, or any text input
- **Video Summarization**: Process video content to generate text-based summaries
- **User Authentication**: Secure signup and login system
- **Responsive Design**: Modern, user-friendly interface with light/dark theme support
- **Content Management**: Track and manage your summarization history

## Technology Stack

### Frontend
- React.js
- React Router for navigation
- CSS3 for styling

### Backend
- Python
- NLTK (Natural Language Toolkit)
- NumPy for numerical computations

### Database
- MySQL

### AI/ML Components
- Extractive Text Summarization using cosine similarity and sentence ranking
- NLTK for tokenization and stopword removal
- Feature extraction for text analysis

## Project Structure

```
concisely/
├── App.js                  # Main application component with routing
├── App.css                 # Global application styles
├── index.js                # Application entry point
├── index.css               # Global styles
├── components/
│   ├── Landing.js          # Landing page
│   ├── Signup.js           # User registration
│   ├── Login.js            # User authentication
│   ├── Home.js             # Main dashboard
│   ├── TextSummary.js      # Text summarization interface
│   ├── VideoSummary.js     # Video summarization interface
│   └── ThemeToggle.js      # Theme switcher
├── text-summarizer.py      # Core text summarization algorithm
├── feature+summary.py      # Enhanced summarization with feature extraction
├── feature_text.py         # Text feature extraction utilities
└── database.sql            # Database schema
```

## Installation

### Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- MySQL Server
- npm or yarn package manager

### Frontend Setup

1. Clone the repository:
```bash
git clone https://github.com/kaniikaaaa/ai-text-and-video-summarizer.git
cd ai-text-and-video-summarizer
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download required NLTK data:
```python
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Database Setup

1. Create the database:
```bash
mysql -u root -p < database.sql
```

2. Configure database connection in your backend files

## How It Works

### Text Summarization Algorithm

The text summarization feature uses an extractive approach:

1. **Tokenization**: Text is split into sentences and words
2. **Preprocessing**: Stopwords are removed and text is normalized
3. **Similarity Matrix**: Cosine similarity is calculated between sentences
4. **Ranking**: Sentences are ranked based on similarity scores
5. **Extraction**: Top-ranked sentences are selected until word limit is reached

### Feature Extraction

The system extracts the following features from input text:
- Total word count
- Total sentence count
- Unique word count
- Most common words
- Average sentence length

## Usage

### Text Summarization

1. Navigate to the Text Summary page
2. Paste or type your text in the input area
3. Specify the desired word limit for the summary
4. Click "Summarize Text" to generate the summary

### Video Summarization

1. Navigate to the Video Summary page
2. Upload your video file
3. Wait for processing
4. View the generated text summary

## Database Schema

The application uses four main tables:

- **users**: Stores user account information
- **files**: Tracks uploaded files and their processing status
- **summaries**: Stores generated summaries
- **login**: Logs user activity and actions

## API Endpoints

Documentation for backend API endpoints will be added as the backend implementation is completed.

## Development

### Available Scripts

- `npm start`: Run the development server
- `npm build`: Build the production application
- `npm test`: Run test suite

### Running Python Scripts

To test the summarization algorithm independently:

```bash
python text-summarizer.py
```

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## Future Enhancements

- Integration with transformer-based models (BART, T5, GPT)
- Real-time video processing
- Multi-language support
- API for third-party integrations
- Export summaries in multiple formats
- Advanced video analysis with scene detection
- Chatbot interface for guided summarization

## Screenshots

![Landing Page](https://github.com/user-attachments/assets/dea8c750-bc26-4eb5-9027-c12d68ae0649)
![Application Interface](https://github.com/user-attachments/assets/1458ba31-329b-47cc-bf47-0890f382bea8)

## License

This project is open source and available for educational purposes.

## Contact

For questions or feedback, please open an issue on the GitHub repository.

## Acknowledgments

- NLTK library for natural language processing tools
- React community for frontend framework
- Contributors and testers who helped improve this project
