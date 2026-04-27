import requests
from requests.exceptions import RequestException
from datetime import datetime
from extraction.config import frankfurter_base_url

def fetch_exchange_rates():
    base_currencies = ["EUR","GBP","JPY"]
    extracted_rates = []

    for base_currency in base_currencies:
        url = f"{frankfurter_base_url}? from = {base_currency} & to = USD"

        try:
            response = requests.get(url, timeout= 15)
            response.raise_for_status()
            data = response.json()

            usd_rate = data.get("rates", {}).get("USD")
            rate_date = data.get("date", datetime.today().strftime("%Y-%m-%d"))     #if for some reason date is missing, it uses today’s date as fallback

            if usd_rate is None:
                print(f"[WARNING] USD rate for {base_currency} is missing")
                continue

            extracted_rates.append({
                "date" : rate_date,
                "base_currency" : base_currency,
                "target_currency" : "USD",
                "exchange_rate" : usd_rate
            })

        except RequestException as e:
            print(f"[ERROR] Failed to fetch exchange rate for {base_currency}: {e}")

    return extracted_rates