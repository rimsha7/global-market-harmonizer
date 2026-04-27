import os
import json
from datetime import datetime

from extraction.config import validate_env
from extraction.extract_exchange_rates import fetch_exchange_rates
from extraction.extract_products import fetch_products
from extraction.upload_to_s3 import upload_file_to_s3


def ensure_directory(path: str):
    os.makedirs(path, exist_ok=True)


def save_json(data, path: str):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def run():
    print("STARTING PIPELINE...")

    validate_env()
    print("Environment validated.")

    today = datetime.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    local_dir = os.path.join("data", "raw", year, month, day)
    ensure_directory(local_dir)
    print(f"Created local directory: {local_dir}")

    exchange_rates = fetch_exchange_rates()
    print(f"Fetched exchange rates: {len(exchange_rates)} records")

    products = fetch_products()
    print(f"Fetched products: {len(products)} records")

    exchange_json_path = os.path.join(local_dir, "exchange_rates.json")
    products_json_path = os.path.join(local_dir, "products.json")

    save_json(exchange_rates, exchange_json_path)
    save_json(products, products_json_path)
    print("Saved JSON files locally.")

    s3_prefix = f"{year}/{month}/{day}"

    upload_file_to_s3(exchange_json_path, f"{s3_prefix}/exchange_rates.json")
    upload_file_to_s3(products_json_path, f"{s3_prefix}/products.json")

    print("[SUCCESS] JSON files extracted, saved locally, and uploaded to S3 successfully.")


if __name__ == "__main__":
    run()