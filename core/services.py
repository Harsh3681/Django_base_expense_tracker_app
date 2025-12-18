import os
import requests

def fetch_exchange_rates(base: str) -> dict:
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise RuntimeError("EXCHANGE_RATE_API_KEY not set in environment")

    base = base.upper().strip()
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"

    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    if data.get("result") != "success":
        raise RuntimeError(f"ExchangeRate API error: {data.get('error-type', 'unknown_error')}")

    return data.get("conversion_rates", {})
