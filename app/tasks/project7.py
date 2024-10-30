import sys

import feedparser
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from app.utils.utils import print_outcome

def is_secure_rss_url(url: str) -> bool:
    if not url.startswith('https://'):
        print("URL must start with 'https://'")
        return False

    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        print("Invalid URL format.")
        return False

    return True

# Function to fetch content from a URL
def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def load_rss_and_extract_content(rss_url):
    feed = feedparser.parse(rss_url)

    links = [entry.link for entry in feed.entries]

    with ThreadPoolExecutor(max_workers=5) as executor:
        contents = list(executor.map(fetch_content, links))

    text_to_print = ""
    for link, content in zip(links, contents):
        if content:
            text_to_print += f"Content from {link}:\n\n{content[:500]}...\n\n\n\n"
    print_outcome(text_to_print)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = sys.argv[1].strip()
        if is_secure_rss_url(user_input):
            load_rss_and_extract_content(user_input)
    else:
        print("Please provide secure rss url in double quotes")

# export PYTHONPATH=$(pwd)