# 📰 AI News Scraper & Realtime Dashboard

This project automatically scrapes **AI-related news headlines** from major tech websites and displays them in a real-time web dashboard. It uses a Python script for scraping and a Node.js server with EJS to display the data.

---

## 🚀 Features

- ✅ Scrapes AI-related news from:
  - [WION Technology](https://www.wionews.com/technology)
  - [BBC Innovation](https://www.bbc.com/innovation)
  - [Bloomberg Technology](https://www.bloomberg.com/technology)
  - [DD News Science & Tech](https://ddnews.gov.in/en/category/science-tech/)
- ✅ Detects AI-related keywords in headlines
- ✅ Extracts headline, URL, source, image, and timestamp
- ✅ Sends news to a local webhook (`http://localhost:3000/webhook`)
- ✅ Stores all entries in `headlines.log`
- ✅ Displays headlines in a responsive EJS dashboard
- ✅ Avoids duplicates (even after restart)

---

## 📁 Project Structure

```
AI-News-Scraper/
│
├── scrapper.py             # Python script for scraping and sending data
├── server.js               # Node.js server (webhook + UI)
├── qr.js                   # Scan for mobile access
├── views/
│   └── index.ejs           # EJS HTML template
├── headlines.log           # Persistent log of all headlines
├── package.json            # Node.js dependencies
└── README.md               # Project documentation
```

---

## 🔧 Requirements

### Python

```bash
pip install requests beautifulsoup4 urllib3
```

### Node.js

```bash
npm install express ejs
```

---

## ⚙️ Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/archakNath/AI-News-Heading-Scrapper
cd AI-News-Heading-Scrapper
```

### 2. Start Node.js server

```bash
node server.js
```

Runs at: [http://localhost:3000](http://localhost:3000)

### 3. Start the Python scraper

```bash
python scrapper.py
```

The scraper runs every 60 seconds and sends AI-related headlines to the local server.

---

## 🌐 Dashboard

Visit in browser:

```
http://localhost:3000
```

You’ll see:
- 📰 Headline (linked)
- 📸 Image preview (or placeholder)
- 🌍 Source (WION, BBC, Bloomberg, DD News)
- ⏱️ Timestamp

The dashboard is mobile responsive ✅

---

## 📤 Sample Webhook Payload

```json
{
  "headline": "OpenAI launches GPT-5",
  "url": "https://www.bbc.com/news/articles/openai-gpt5",
  "source": "BBC",
  "image": "https://bbc.com/image.jpg",
  "time": "12/07/2025, 09:15:30 PM"
}
```

---

## 🧠 Optional Improvements

- 💾 Store headlines in MongoDB or SQLite
- 🔍 Add frontend search or filters by source/date
- 🧠 NLP-based topic categorization
- 🌐 Deploy with Render / Railway / Vercel
- 📱 Enable real-time updates with WebSockets

---

## 📲 Access from Mobile

To view on another device (e.g., smartphone):

1. Get your computer’s IP:

   ```bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   ```

2. Make sure both devices are on the same Wi-Fi
3. Visit:

   ```
   http://<your-laptop-ip>:3000
   ```

---

## 📄 License

MIT License  
You’re free to use, modify, and distribute this project with attribution.

---

**Made with ❤️ by [Archak Nath](https://github.com/archakNath)**