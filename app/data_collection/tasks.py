import time

from app.data_collection.celery_app import celery_app
from app.database import SessionLocal
from app.data_collection.deribit import get_index_price
from app.models import Price


@celery_app.task(name="app.tasks.fetch_prices")
def fetch_prices():
    tickers = ["btc_usd", "eth_usd"]

    with SessionLocal() as db:
        for ticker in tickers:
            try:
                price = get_index_price(ticker)

                record = Price(
                    ticker=ticker,
                    price=price,
                    timestamp=int(time.time()),
                )

                db.add(record)
                db.commit()

            except Exception:
                db.rollback()
                raise