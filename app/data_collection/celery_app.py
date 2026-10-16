from celery import Celery

celery_app = Celery(
    "deribit_tracker",
    broker="redis://localhost:6379/0",
    include=["app.tasks"],
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.fetch_prices",
        "schedule": 60.0,
    },
}

celery_app.conf.timezone = "UTC"