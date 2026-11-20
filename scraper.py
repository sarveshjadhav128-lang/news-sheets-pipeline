import csv
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

URL = "https://news.ycombinator.com/"
OUTPUT_CSV = "headlines.csv"


def scrape_news(url: str) -> list[dict[str, str]]:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = []

    # Example selector structure; adjust selectors to match your chosen public news page
    for item in soup.select("tr.athing"):
        title_link = item.select_one("span.titleline > a")
        if not title_link:
            continue

        headline = title_link.get_text(strip=True)
        link = urljoin(url, title_link.get("href", "").strip())

        meta_row = item.find_next_sibling("tr")
        age_el = meta_row.select_one("span.age") if meta_row else None
        date_or_age = age_el.get_text(strip=True) if age_el else "N/A"

        rows.append({
            "headline": headline,
            "date": date_or_age,
            "url": link,
        })

    return rows


def save_to_csv(rows: list[dict[str, str]], filename: str) -> None:
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["headline", "date", "url"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    scraped = scrape_news(URL)
    save_to_csv(scraped, OUTPUT_CSV)
    print(f"Saved {len(scraped)} rows to {OUTPUT_CSV}")