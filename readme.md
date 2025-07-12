
# 📰 AI News Scraper & Real-Time Web Dashboard

This project is a Python + Node.js-based system that scrapes AI-related headlines from top tech news websites and streams them live to a real-time web dashboard using WebSockets.

---

## 📌 Features

- 🔎 Scrapes AI-related news from:
  - [WION](https://www.wionews.com/technology)
  - [BBC](https://www.bbc.com/innovation)
  - [Bloomberg Technology](https://www.bloomberg.com/technology)
  - [DD News](https://ddnews.gov.in/en/category/science-tech/)
- 📡 Real-time updates using **Socket.IO**
- 🧠 Filters only AI-related headlines using simple NLP logic
- 🖼️ Displays images with fallback placeholders
- 📝 Stores headlines locally in `headlines.log`
- 🌐 Beautiful responsive web dashboard with EJS
- 🔄 Refreshes the UI in real-time when new data arrives via webhook

---

## 📂 Project Structure

```
AI-News-Heading-Scraper/
├── scrapper.py             # Python script for scraping all sources
├── server.js               # Node.js Express server with Socket.IO
├── views/
│   └── index.ejs           # Real-time EJS frontend
├── public/                 # Static JS/CSS if needed
├── headlines.log           # Local log of all received headlines
├── package.json            # Node.js dependencies
└── README.md               # This documentation
```

---

## 🔧 Prerequisites

- Python 3.x
- Node.js (v14+ recommended)
- `pip` & `npm` package managers

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/archakNath/AI-News-Heading-Scrapper
cd AI-News-Heading-Scrapper
```

### 2. Install Node.js Dependencies

```bash
npm install express ejs socket.io
```

### 3. Run the Node.js Server

```bash
node server.js
```

Visit the dashboard at:  
👉 http://localhost:3000

### 4. Install Python Requirements

```bash
pip install requests beautifulsoup4 urllib3
```

### 5. Run the Python Scraper

```bash
python scrapper.py
```

This will:
- Continuously scrape from all four sources every 60 seconds
- Detect AI-related headlines
- Send new headlines to your server via `/webhook`

---

## 🌐 Web Dashboard

- Built with **EJS**
- Automatically updates in real-time using **Socket.IO**
- Mobile responsive and image-friendly
- Displays source, time, and fallback placeholder if image is missing

---

## 📦 Example Webhook Payload

```json
{
  "headline": "AI helps doctors detect rare disease faster",
  "url": "https://example.com/news",
  "source": "BBC",
  "time": "12/07/2025, 10:19:35 PM",
  "image": "https://example.com/image.jpg"
}
```

---

## 💡 Future Enhancements

- 🌍 Add global news aggregators (e.g., TechCrunch, Reuters AI, etc.)
- 📊 Search & filter UI (by source/date/keyword)
- 🧠 Use NLP/ML to auto-summarize headlines
- 💾 Add MongoDB or SQLite for persistent DB storage
- ☁️ Deploy full-stack project using Render, Vercel or Railway

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to fork, modify, and contribute!

> Created with ❤️ by [@archakNath](https://github.com/archakNath)
