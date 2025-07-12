const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const fs = require("fs");
const path = require("path");
const { Server } = require("socket.io");

const io = new Server(server); // socket.io server
const PORT = 3000;
const LOG_FILE = "headlines.log";

app.use(express.json());
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static("public")); // for frontend JS

let headlinesData = [];

// Load existing headlines from log on startup
function loadHeadlinesFromLog() {
    if (!fs.existsSync(LOG_FILE)) return;

    const lines = fs.readFileSync(LOG_FILE, "utf-8").split("\n").filter(Boolean);
    const seen = new Set();

    headlinesData = lines.map(line => {
        try {
            const entry = JSON.parse(line);
            if (!seen.has(entry.headline)) {
                seen.add(entry.headline);
                return entry;
            }
        } catch (err) {
            console.error("Error parsing log line:", line);
        }
        return null;
    }).filter(Boolean);
}

// Save headline and notify clients
function saveHeadline(entry) {
    if (headlinesData.find(h => h.headline === entry.headline)) {
        return;
    }

    headlinesData.unshift(entry);

    fs.appendFile(LOG_FILE, JSON.stringify(entry) + "\n", (err) => {
        if (err) console.error("Error writing to log:", err);
    });

    io.emit("new-headline", entry); // broadcast to all clients
}

// Webhook
app.post("/webhook", (req, res) => {
    const { headline, url, source, time, image } = req.body;

    if (!headline || !url || !source || !time) {
        return res.status(400).send("Missing one or more fields");
    }

    const entry = { headline, url, source, time, image };
    saveHeadline(entry);

    console.log("Received:", entry);
    res.status(200).send("Received");
});

// Homepage
app.get("/", (req, res) => {
    const sortedHeadlines = [...headlinesData].sort((a, b) => {
        return new Date(b.time) - new Date(a.time); // Descending order
    });
    res.render("index", { headlines: sortedHeadlines });
});


// Load existing headlines
loadHeadlinesFromLog();

// Start the server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
