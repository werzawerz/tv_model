from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_product_details_from_url(_url):
    response = requests.get(_url)
    soup = BeautifulSoup(response.text)

    details_map = {}

    # Get product details
    technikai_jellemzok = soup.findAll('dl', {'class': 'specification'})
    for dl in technikai_jellemzok:
        dt_elements = dl.find_all('dt')
        dd_elements = dl.find_all('dd')
    
        # Extract and store the key-value pairs in the dictionary
        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.get_text(strip=True)
            value = dd.get_text(strip=True)
            details_map[key] = value

    # Get product price
    price_div = soup.find("div", {"class": "price big"})
    details_map["price"] = price_div.get_text(strip=True)

    return details_map


def get_product_details_map(urls):
    product_details = []
    for i, tv_list_url in enumerate(urls):
        print(i)
        response = requests.get(tv_list_url)
        soup = BeautifulSoup(response.text)
        tv_list = soup.findAll('div', {'class': 'product-wrapper'})

        product_urls = []
        product_url_start = "https://www.mediamarkt.hu/hu/product/"
        for tv in tv_list:
            a_elem = tv.find_all("a", href=lambda href: href and href.startswith(product_url_start))
            url = a_elem[0]["href"]
            product_urls.append(url)


        for product_url in product_urls:
            product_details.append(
                get_product_details_from_url(product_url)
            )

    return product_details


if __name__ == "__main__":
    urls = []
    for i in range(1, 14):
        urls.append(
            f"https://www.mediamarkt.hu/hu/category/_4k-uhd-tv-679556.html?searchParams=&sort=&view=&page={i}"
        )

    product_details = get_product_details_map(urls)

    df = pd.DataFrame(product_details)
    df.to_parquet("tv_data.parquet")