import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

base_url = "https://books.toscrape.com/"
current_url = base_url

data = []

while current_url:
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]

        price_text = book.select_one(".price_color").get_text(strip=True)
        price = price_text.replace("Â£", "").replace("£", "").strip()
        price = float(price)

        rating = book.select_one(".star-rating")["class"][1]
        availability = book.select_one(".availability").get_text(strip=True)
        book_url = urljoin(base_url, book.h3.a["href"])

        data.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability,
            "URL": book_url
        })

    next_button = soup.select_one("li.next a")

    if next_button:
        current_url = urljoin(current_url, next_button["href"])
    else:
        current_url = None

df = pd.DataFrame(data)

df.to_csv("data/books.csv", index=False, encoding="utf-8-sig")

print(f"Successfully scraped {len(df)} books.")
print("Dataset saved to data/books.csv")
