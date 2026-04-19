# Concisely

Summarizes articles, PDFs, and YouTube videos with a hybrid extractive + abstractive pipeline. Long inputs are compressed by TextRank, then refined by BART, so summaries stay faithful without blowing the model's context window.

## Stack

React · Flask · TextRank · BART (HuggingFace Transformers) · TF-IDF · NLTK · youtube-transcript-api · PyPDF2

## What's interesting here

- **Extractive then abstractive, not one or the other.** TextRank + TF-IDF pick the top-ranked sentences; BART rewrites that distillation into natural prose. Full-transformer summarization on a 30-minute YouTube transcript is a non-starter for latency and memory; this pipeline is.
- **Transcript path for YouTube.** Uses `youtube-transcript-api` to pull the captions track directly, so videos are summarized without downloading or transcribing audio.
- **Frontend is React + CRA, backend is Flask with CORS; strict separation.** The summarizer runs as a standalone Flask service, so the pipeline can be swapped or scaled independently of the UI.

## Run locally

```bash
git clone https://github.com/kaniikaaaa/ai-text-and-video-summarizer.git
cd ai-text-and-video-summarizer

# Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python backend_api.py   # http://localhost:5000

# Frontend (new terminal)
cd frontend   # or wherever the CRA app lives
npm install
npm start     # http://localhost:3000
```

First run downloads the BART checkpoint (~1.6 GB) to the HuggingFace cache.

## Endpoints

```
POST /summarize         Body: { "text": "..." }              -> summary of raw text
POST /summarize-pdf     multipart: file                      -> summary of PDF
POST /summarize-video   Body: { "url": "https://youtu.be/..." } -> summary of YouTube transcript
```

## License

MIT
