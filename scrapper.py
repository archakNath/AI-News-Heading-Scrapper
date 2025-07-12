import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

WEBHOOK_URL = "http://localhost:3000/webhook"
LOG_FILE = "headlines.log"

# Load already sent headlines
def load_sent_headlines():
    sent = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    sent.add(data["headline"])
                except json.JSONDecodeError:
                    continue
    return sent

# Save to local log file
def save_to_log(entry):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + "\n")

# Simple AI-related keyword check
def is_ai(headline):
    words = headline.lower().split()
    if "ai" in words:
        return True
    for word in words:
        if word.endswith("ai"):
            return True
    return False

# Send data to webhook server
def send_to_webhook(headline, url, source, image=None):
    entry = {
        "headline": headline,
        "url": url,
        "source": source,
        "image": image,
        "time": datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
    }
    try:
        response = requests.post(WEBHOOK_URL, json=entry)
        if response.status_code == 200:
            print(f"Sent to server: {headline}")
            save_to_log(entry)
            return True
        else:
            print(f"Failed to send: {headline} | Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending {headline}: {e}")
    return False


# WION Scraper
def scrape_wion(sent):
    print("Scraping WION...")
    base_url = "https://www.wionews.com"
    url = f"{base_url}/technology"
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, "html.parser")
        for card in soup.select("div.ui-componets_headingH3__beR_u"):
            a_tag = card.find("a")
            if not a_tag:
                continue
            headline = a_tag.get_text(strip=True)
            link = a_tag.get("href")
            if link and not link.startswith("http"):
                link = base_url + link

            # Try to find image nearby (adjust if needed)
            img_tag = card.find_previous("img")
            image_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

            if headline and is_ai(headline) and headline not in sent:
                if send_to_webhook(headline, link, "WION", image_url):
                    sent.add(headline)
    except Exception as e:
        print(f"Error scraping WION: {e}")


# BBC Scraper
def scrape_bbc(sent):
    print("Scraping BBC...")
    url = "https://www.bbc.com/innovation"
    base_url = "https://www.bbc.com"
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, "html.parser")

        for wrapper in soup.select('div[data-testid="anchor-inner-wrapper"]'):
            a_tag = wrapper.find("a")
            if not a_tag:
                continue

            headline_elem = a_tag.select_one('h2[data-testid="card-headline"]')
            if not headline_elem:
                continue

            headline = headline_elem.get_text(strip=True)
            article_url = a_tag.get("href")
            if article_url and not article_url.startswith("http"):
                article_url = base_url + article_url

            # Get real image URL (ignore placeholders)
            img_tag = wrapper.select_one("img")
            image_url = None

            if img_tag:
                # Check srcset first
                if img_tag.has_attr("srcset"):
                    srcset_entries = img_tag["srcset"].split(",")
                    # Get highest quality image (last one)
                    candidates = [entry.strip().split(" ")[0] for entry in srcset_entries]
                    # Filter out placeholders
                    valid_images = [url for url in candidates if "placeholder" not in url]
                    if valid_images:
                        image_url = valid_images[-1]  # Pick largest
                # Fallback to src if no valid srcset
                if not image_url and img_tag.has_attr("src"):
                    if "placeholder" not in img_tag["src"]:
                        image_url = img_tag["src"]

            if headline and is_ai(headline) and headline not in sent:
                if send_to_webhook(headline, article_url, "BBC", image_url):
                    sent.add(headline)

    except Exception as e:
        print(f"Error scraping BBC: {e}")


# Bloomberg scrapper
def scrape_bloomberg(sent):
    print("Scraping Bloomberg...")
    url = "https://www.bloomberg.com/technology"
    base_url = "https://www.bloomberg.com"
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, "html.parser")

        cards = soup.select('div.LineupContent3Up_item__xPppd')
        for card in cards:
            # Get headline text
            headline_span = card.select_one('div[data-testid="headline"] span')
            if not headline_span:
                continue
            headline = headline_span.get_text(strip=True)

            # Get article URL
            link_tag = card.find("a", href=True)
            article_url = link_tag['href']
            if article_url and not article_url.startswith("http"):
                article_url = base_url + article_url

            # Get image
            img_tag = card.select_one("img")
            image_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

            # Filter AI-related and unsent
            if headline and is_ai(headline) and headline not in sent:
                if send_to_webhook(headline, article_url, "Bloomberg", image_url):
                    sent.add(headline)

    except Exception as e:
        print(f"Error scraping Bloomberg: {e}")

# DD News
def scrape_ddnews(sent):
    print("Scraping DD News...")
    url = "https://ddnews.gov.in/en/category/science-tech/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://ddnews.gov.in/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        resp = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        for article in soup.select("article.post"):
            title_elem = article.select_one("h2.entry-title a")
            if not title_elem:
                continue

            headline = title_elem.get_text(strip=True)
            article_url = title_elem["href"]
            if not article_url.startswith("http"):
                article_url = "https://ddnews.gov.in" + article_url

            # Time string
            time_elem = article.select_one("p.mb-0.colorPrimary.fs-14")
            timestamp = time_elem.get_text(strip=True) if time_elem else datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")

            # Image
            img_tag = article.select_one("figure.featured-media img")
            image_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

            # Only send if headline contains AI
            if headline and is_ai(headline) and headline not in sent:
                if send_to_webhook(headline, article_url, "DD News", image_url):
                    sent.add(headline)

    except Exception as e:
        print(f"Error scraping DD News: {e}")



# Main loop
def main():
    sent_headlines = load_sent_headlines()
    while True:
        scrape_wion(sent_headlines)
        scrape_bbc(sent_headlines)
        scrape_bloomberg(sent_headlines)
        scrape_ddnews(sent_headlines)
        print("Waiting 60 seconds...\n")
        time.sleep(60)


if __name__ == "__main__":
    main()
