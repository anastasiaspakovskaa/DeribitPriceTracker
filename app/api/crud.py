from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Price


def get_prices(db: Session, ticker: str) -> list[Price]:
    statement = (
        select(Price)
        .where(Price.ticker == ticker)
        .order_by(Price.timestamp)
    )
    return list(db.scalars(statement).all())


def get_latest_price(db: Session, ticker: str) -> Price | None:
    statement = (
        select(Price)
        .where(Price.ticker == ticker)
        .order_by(Price.timestamp.desc(), Price.id.desc())
        .limit(1)
    )
    return db.scalars(statement).first()


def get_prices_from_date(
    db: Session,
    ticker: str,
    start_date: int,
    end_date: int,
) -> list[Price]:
    statement = (
        select(Price)
        .where(
            Price.ticker == ticker,
            Price.timestamp >= start_date,
            Price.timestamp <= end_date,
        )
        .order_by(Price.timestamp)
    )
    return list(db.scalars(statement).all())