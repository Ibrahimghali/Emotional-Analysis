# 🧠 Depression Analysis Project

## 📘 Overview

This project analyzes depression-related content from Twitter to uncover **patterns**, **sentiments**, and **topics**. It features a FastAPI backend that:

* Scrapes tweets using the Twitter API
* Cleans and normalizes text data
* Performs sentiment analysis via Hugging Face transformers (DistilBERT)
* Detects topics based on keyword matching
* Stores results in MongoDB for later access and visualization

---

## ✨ Key Features

* ✅ Twitter data scraping with Bearer Token support and rate limit handling
* ✅ Text preprocessing: cleaning, normalization, and stopword removal
* ✅ Sentiment classification using DistilBERT
* ✅ Rule-based topic detection
* ✅ RESTful API for triggering scraping and retrieving posts
* ✅ Asynchronous background processing with FastAPI

---

## 🧱 Architecture

```
 ┌────────────┐    ┌─────────────┐    ┌─────────────────┐
 │ FastAPI    │ →  │ Text        │ →  │ Sentiment &     │
 │ Backend    │    │ Processing  │    │ Topic Detection │
 └────┬───────┘    └────┬────────┘    └────┬────────────┘
      │                │                 │
      ▼                ▼                 ▼
 ┌────────────┐    ┌────────────┐    ┌──────────────┐
 │ Twitter    │    │ NLP Utils  │    │ MongoDB      │
 │ Scraper    │    │ (Cleaning) │    │ Storage      │
 └────────────┘    └────────────┘    └──────────────┘
```

---

## ⚙️ Installation & Setup

### 🔧 Requirements

* Python 3.8+
* Twitter API Bearer Token
* Docker & Docker Compose

### 🚀 Quickstart

1. **Clone the repository**

```bash
git clone https://github.com/Ibrahimghali/depression-analysis.git
cd depression-analysis
```

2. **Create `.env` file for Twitter API**

```env
TWITTER_BEARER_TOKEN=your_token_here
```

---

## ▶️ Run the Application (Docker Compose)

Build and start the containers:

```bash
docker-compose up --build
```

To run in the background:

```bash
docker-compose up -d
```

Check container status:

```bash
docker-compose ps
```

Once running, open your browser at:
📄 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

| Method | Endpoint      | Description                               |
| ------ | ------------- | ----------------------------------------- |
| POST   | `/api/scrape` | Start Twitter scraping (async)            |
| GET    | `/api/posts`  | Retrieve all processed posts from MongoDB |

---

## 🧪 Testing

Run tests with:

```bash
python -m pytest tests/
```

Test cases cover:

* URL and emoji removal
* Text normalization
* Stopword removal
* Edge cases in preprocessing

---

## 📁 Project Structure

```
depression-analysis/
├── app/
│   ├── main.py                  # Entry point
│   ├── api/routes.py            # REST API endpoints
│   ├── database/mongodb.py      # MongoDB connection
│   ├── nlp/
│   │   ├── sentiment_analyzer.py
│   │   ├── text_processor.py
│   │   └── topic_detector.py
│   └── scraper/twitter_scraper.py
└── tests/
    └── test_text_processor.py
```

---
