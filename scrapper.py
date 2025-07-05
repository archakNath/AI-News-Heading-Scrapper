import requests
from bs4 import BeautifulSoup
import time

WEBHOOK_URL = "http://localhost:3000/webhook"

def is_ai(headline):
    words = headline.lower().split()

    # Check if any word is exactly "ai"
    if "ai" in words:
        return True

    # Check if any word ends with "ai"
    for word in words:
        if word.endswith("ai"):
            return True

    return False

def send_to_webhook(headline):
    data = {
        "headline": headline
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 200:
            print(f"Sent: {headline}")
        else:
            print(f"Failed to send: {headline} | Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending {headline}: {e}")

def scrape_headlines():
    url = "https://www.wionews.com/technology"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select("h3"):
        text = item.get_text(strip=True)
        if text and is_ai(text):
            print(f"Found: {text}")
            send_to_webhook(text)

if __name__ == "__main__":
    while True:
        scrape_headlines()
        print("Waiting...\n")
        time.sleep(60)
