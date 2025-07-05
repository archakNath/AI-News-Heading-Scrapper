# 📰 AI News Scraper & Webhook Dashboard

This project scrapes AI-related news headlines from tech news websites and sends them in real-time to a Node.js webhook server. The headlines are stored and displayed on a web dashboard using EJS.

---

## 📌 Features

- Scrapes AI-related headlines from [WION Technology](https://www.wionews.com/technology)
- Detects headlines containing or ending with the word "AI"
- Sends headlines to a local webhook via HTTP POST
- Node.js server logs and displays headlines using an EJS dashboard

---

## 📂 Project Structure

```
project/
│
├── scrapper.py             # Python script for scraping and sending data
├── server.js               # Node.js Express server to receive and display data
├── views/
│   └── index.ejs           # EJS template for viewing headlines
├── headlines.log           # Log file storing received headlines
├── package.json            # Node.js dependencies
└── README.md               # Project documentation
```

---

## 🔧 Prerequisites

- Python 3.x
- Node.js (v14 or later)
- pip (Python package manager)
- npm (Node.js package manager)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-news-scraper.git
cd ai-news-scraper
```

### 2. Install Node.js Dependencies

```bash
npm install express ejs
```

### 3. Run the Node.js Server

```bash
node server.js
```

The server will be running at [http://localhost:3000](http://localhost:3000)

### 4. Install Python Requirements

```bash
pip install requests beautifulsoup4
```

### 5. Run the Python Scraper

```bash
python scrapper.py
```

The scraper will:
- Visit WION Technology page every 60 seconds
- Detect headlines containing or ending with "AI"
- Send them to the webhook server

---

## 🌐 Web Dashboard

Visit:

```
http://localhost:3000
```

You’ll see a list of all AI-related headlines received so far.

---

## 📒 Example Webhook Payload

```json
{
  "headline": "AI helps doctors detect rare disease faster"
}
```

---

## 🧹 Optional Enhancements

- Add support for more websites (BBC, Bloomberg, etc.)
- Filter duplicate headlines
- Store headlines in a database (e.g., MongoDB or SQLite)
- Add search or filtering in the frontend
- Deploy on cloud (Render, Vercel, Heroku)

---

## 📄 License

This project is licensed under the MIT License. Feel free to use and modify it as needed.
