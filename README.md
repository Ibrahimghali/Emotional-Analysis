
# 🧠 Depression Analysis Project

## 📖 Overview
This project analyzes depression-related content from social media (Twitter) to identify **patterns**, **sentiments**, and **topics**. It provides a FastAPI backend that:

- Scrapes Twitter using the official API,
- Processes the text (cleaning and normalization),
- Performs sentiment analysis using Hugging Face models,
- Detects topics based on keywords,
- Stores results in MongoDB for retrieval and visualization.

---

## ✨ Features

- ✅ Twitter data scraping with rate limit handling (Bearer Token)
- ✅ Text cleaning and normalization
- ✅ Sentiment analysis using DistilBERT
- ✅ Topic detection via keyword matching
- ✅ REST API endpoints for triggering and retrieving data
- ✅ Asynchronous background processing

---

##  🧱 System Architecture

    

    ┌────────────┐    ┌─────────────┐    ┌───────────────┐
    │ FastAPI    │    │ Text        │    │ Sentiment     │
    │ Backend    │───>│ Processing  │───>│ Analysis &    │
    └────────────┘    └─────────────┘    │Topic Detection│
    │                                    └───────────────┘
    │                                       │
    ▼                                       ▼
    ┌────────────┐                       ┌───────────────┐
    │ Twitter    │                       │ MongoDB       │
    │ Scraper    │                       │ Database      │
    └────────────┘                       └───────────────┘

    

---

## ⚙️ Installation

### 🔧 Prerequisites

- Python 3.8+
- MongoDB (local or Docker)
- Twitter API Bearer Token

---

### 🚀 Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/depression-analysis.git
cd depression-analysis
````

Create and activate a virtual environment:

```bash
python -m venv .venv

# On Windows
.\.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your Twitter API credentials:

```env
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
```

---

### 🗃️ Start MongoDB (via Docker)

```bash
docker run -d -p 27017:27017 --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo
```

---

## ▶️ Running the Application

Start the API server:

```bash
python -m app.main
```

Then open your browser to access API docs:

📄 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

| Method | Endpoint      | Description                              |
| ------ | ------------- | ---------------------------------------- |
| POST   | `/api/scrape` | Triggers Twitter scraping asynchronously |
| GET    | `/api/posts`  | Retrieves all processed posts from DB    |

---

## 🧪 Testing

### ✅ Running Tests

Run all tests with verbose output:

```bash
python -m pytest tests/
```

### 🧼 Test Coverage

The tests verify:

* URL and emoji removal
* Text normalization
* Stopword removal
* Robust text handling

---

## 📁 Project Structure

```
depression-analysis/
├── app/
│   ├── main.py                  # FastAPI application entry
│   ├── api/
│   │   └── routes.py            # API routes
│   ├── database/
│   │   └── mongodb.py           # MongoDB connection logic
│   ├── nlp/
│   │   ├── sentiment_analyzer.py # Sentiment analysis (transformers)
│   │   ├── text_processor.py     # Text cleaning and normalization
│   │   └── topic_detector.py     # Keyword-based topic detection
│   └── scraper/
│       └── twitter_scraper.py    # Twitter API scraper
└── tests/
    └── test_text_processor.py    # Unit tests for text processing
```

---



