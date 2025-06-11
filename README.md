# 🧠 TDS Virtual TA – Tools in Data Science Project

This is a full-stack AI-powered virtual teaching assistant for the *Tools in Data Science* course at IITM. It can answer student questions using scraped context from the course GitHub repo and Discourse forum, and respond via a Flask API using an AI model (e.g., GPT-4o-mini via AI Proxy).

---

## 📦 Features

- Accepts student questions (with optional image)
- Uses OCR (for base64 images)
- Retrieves relevant context from course material
- Queries AI via **AI Proxy**
- Returns structured JSON response
- Ready for promptfoo evaluation with provided YAML

---

## 🛠️ Setup Instructions

### 1. 🔁 Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/tds-virtual-ta.git
cd tds-virtual-ta
