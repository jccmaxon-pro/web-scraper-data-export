import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def extract_number(text: str) -> float | None:
    if not text:
        return None

    cleaned = re.sub(r"[^\d.]", "", text)
    return float(cleaned) if cleaned else None


def parse_properties(html: str, base_url: str | None = None) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    properties = []

    cards = soup.select("article.product_pod")

    for card in cards:
        title_tag = card.select_one("h3 a")
        price_tag = card.select_one(".price_color")
        availability_tag = card.select_one(".availability")
        link_tag = card.select_one("h3 a")

        title = title_tag["title"].strip() if title_tag and title_tag.has_attr("title") else ""
        price_text = price_tag.get_text(strip=True) if price_tag else ""
        availability = availability_tag.get_text(strip=True) if availability_tag else ""

        raw_link = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""
        full_link = urljoin(base_url, raw_link) if base_url and raw_link else raw_link

        properties.append({
            "titulo": title,
            "precio_texto": price_text,
            "precio": extract_number(price_text),
            "ubicacion": "N/A",
            "metros_texto": "N/A",
            "metros": None,
            "disponibilidad": availability,
            "enlace": full_link,
        })

    return properties