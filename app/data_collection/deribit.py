import httpx

DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_index_price"


def get_index_price(ticker: str) -> float:
    response = httpx.get(
        DERIBIT_URL,
        params={"index_name": ticker},
        timeout=10.0,
    )
    response.raise_for_status()

    data = response.json()
    return float(data["result"]["index_price"])