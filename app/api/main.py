from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from datetime import date, datetime, time, timezone

from app.api.crud import (
    get_latest_price,
    get_prices,
    get_prices_from_date,
)
from app.database import SessionLocal
from app.api.schemas import PriceResponse

app = FastAPI(title="Deribit Price Tracker")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_ticker(ticker: str) -> str:
    if ticker not in {"btc_usd", "eth_usd"}:
        raise HTTPException(
            status_code=400,
            detail="ticker must be btc_usd or eth_usd",
        )
    return ticker


@app.get("/prices", response_model=list[PriceResponse])
def read_prices(
    ticker: str = Query(..., description="btc_usd or eth_usd"),
    db: Session = Depends(get_db),
):
    validate_ticker(ticker)
    return get_prices(db, ticker)


@app.get("/prices/latest", response_model=PriceResponse)
def read_latest_price(
    ticker: str = Query(..., description="btc_usd or eth_usd"),
    db: Session = Depends(get_db),
):
    validate_ticker(ticker)
    price = get_latest_price(db, ticker)

    if price is None:
        raise HTTPException(status_code=404, detail="No prices found")

    return price


@app.get("/prices/by-date", response_model=list[PriceResponse])
def read_prices_by_date(
    ticker: str = Query(..., description="btc_usd or eth_usd"),
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    validate_ticker(ticker)

    if start_date >= end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be less than end_date",
        )
    
    start_datetime = datetime.combine(
        start_date, time.min, tzinfo=timezone.utc
    )
    end_datetime = datetime.combine(
        end_date, time.max, tzinfo=timezone.utc
    )
    
    return get_prices_from_date(
        db, 
        ticker, 
        int(start_datetime.timestamp()), 
        int(end_datetime.timestamp())
    )