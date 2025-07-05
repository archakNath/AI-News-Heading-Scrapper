const express = require("express");
const app = express();
const fs = require("fs");
const path = require("path");
const PORT = 3000;

app.use(express.json());
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

let headlinesData = [];

// Webhook
app.post("/webhook", (req, res) => {
    const { headline } = req.body;

    if (!headline) {
        return res.status(400).send("Headline missing");
    }

    const entry = {
        headline,
        time: new Date().toLocaleString()
    };

    headlinesData.unshift(entry);

    fs.appendFile("headlines.log", JSON.stringify(entry) + "\n", (err) => {
        if (err) console.error("Error writing to log:", err);
    });

    console.log("Received:", entry);
    res.status(200).send("Received");
});

// show headlines
app.get("/", (req, res) => {
    res.render("index", { headlines: headlinesData });
});

app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});
