import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

custom_headers = {
    "accept-language": "en-GB,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}


def get_product_info(url):
    response = requests.get(url, headers=custom_headers)
    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")

    title_element = soup.select_one("#productTitle")
    title = title_element.text.strip() if title_element else None

    price_element = soup.select_one("#price_inside_buybox")
    price = price_element.text if price_element else None
    print(price)
    rating_element = soup.select_one("#acrPopover")
    rating_text = rating_element.attrs.get("title") if rating_element else None
    rating = rating_text.replace("out of 5 stars", "") if rating_text else None

    image_element = soup.select_one("#landingImage")
    image = image_element.attrs.get("src") if image_element else None

    description_element = soup.select_one("#productDescription")
    description = description_element.text.strip() if description_element else None

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "image": image,
        "description": description,
        "url": url,
    }


def parse_listing(listing_url):
    response = requests.get(listing_url, headers=custom_headers)
    soup_search = BeautifulSoup(response.text, "lxml")
    link_elements = soup_search.select("[data-asin] h2 a")
    page_data = []
    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get("href"))
        print(f"Scraping product from {full_url[:100]}", flush=True)
        product_info = get_product_info(full_url)
        page_data.append(product_info)

    # next_page_el = soup_search.select_one('a:-soup-contains("Next")')
    # if next_page_el:
    #     next_page_url = next_page_el.attrs.get('href')
    #     next_page_url = urljoin(listing_url, next_page_url)
    #     print(f'Scraping next page: {next_page_url}', flush=True)
    #     page_data += parse_listing(next_page_url)

    return page_data


def main():
    data = []
    search_url = "https://www.amazon.com/iPhone-Charger-Certified%E3%80%91-Lightning-AirPods/dp/B08P25VBY1"
    data = parse_listing(search_url)
    df = pd.DataFrame(data)
    df.to_csv('amz.csv')


if __name__ == '__main__':
    main()
