import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "http://quotes.toscrape.com"
OUTPUT = "quotes.csv"

def scrape_quotes():
    all_quotes = []
    page = 1

    while True:
        print(f"Scraping page {page}...")
        response = requests.get(f"{URL}/page/{page}/")

        if response.status_code != 200:
            print("Failed to fetch page.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            print("No more quotes found.")
            break

        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            author_link = quote.find("small", class_="author").find_next("a")
            author_url = URL + author_link.get("href")
            all_quotes.append({
                "text": text,
                "author": author,
                "tags": ", ".join(tags),
                "author_url": author_url
            })

        page += 1

    return all_quotes


def save_to_csv(quotes):
    file_exists = os.path.exists(OUTPUT)
    with open(OUTPUT, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags", "author_url"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(quotes)
    print(f"Saved {len(quotes)} quotes to {OUTPUT}")

def print_summary(quotes):
    author_counts= {}
    for q in quotes:
        author = q["author"]
        author_counts[author] = author_counts.get(author, 0 )+1
    print(f"Scraped {len(quotes)} quotes")
    print(f'{"Top 5 authors:":<5}')
    for auth, total in sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{auth}: {total} quotes")

if __name__ == "__main__":
    quotes = scrape_quotes()
    save_to_csv(quotes)
    print_summary(quotes)