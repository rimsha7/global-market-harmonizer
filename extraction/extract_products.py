import requests
from requests.exceptions import RequestException
from extraction.config import fakestore_base_url

def fetch_products():
    try:
        response = requests.get(fakestore_base_url, timeout= 15)
        response.raise_for_status()
        products = response.json()

        cleaned_products = []

        for product in products:
            rating = product.get("rating", {}) or {}

            cleaned_products.append({
                "product_id" : product.get("id"),
                "product_title" : product.get("title"),
                "price" : product.get("price"),
                "product_category" : product.get("category"),
                "description" : product.get("description"),
                "rating_rate": rating.get("rate"),
                "rating_count": rating.get("count")
            })

        return cleaned_products
    
    except RequestException as e:
        print(f"[ERROR] Failed to fetch products: {e}")
        return[]