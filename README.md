# Deribit Price Tracker

Приложение для сбора и хранения индексных цен BTC и ETH с криптобиржи Deribit.

Данные собираются каждую минуту и сохраняются в PostgreSQL. FastAPI предоставляет API для получения сохранённых цен.

## Установка и запуск

### 1. Клонирование проекта

```bash
git clone https://github.com/anastasiaspakovskaa/DeribitPriceTracker.git
cd DeribitPriceTracker
```

### 2. Создание виртуального окружения

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

```Command prompt
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка PostgreSQL

Создайте базу данных:

```sql
CREATE DATABASE deribit_tracker;
```

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/deribit_tracker
```

Замените `your_password` на пароль PostgreSQL.

Создайте таблицу:

```bash
python -m app.init_db
```

### 5. Запуск Redis

Запустите локальный Redis на порту `6379`.

### 6. Запуск Celery Worker

В отдельном терминале:

```powershell
celery -A app.data_collection.celery_app:celery_app worker --loglevel=info --pool=solo
```

### 7. Запуск Celery Beat

В другом терминале:

```powershell
celery -A app.data_collection.celery_app:celery_app beat --loglevel=info
```

Celery Beat запускает задачу сбора цен каждую минуту.

### 8. Запуск API

```powershell
uvicorn app.api.main:app --reload
```

Документация API доступна по адресу:

http://127.0.0.1:8000/docs

## API

### Получение всех цен

```http
GET /prices?ticker=btc_usd
```

Возвращает все сохранённые цены указанной валюты.

### Получение последней цены

```http
GET /prices/latest?ticker=btc_usd
```

Возвращает последнюю сохранённую цену.

### Получение цен за период

```http
GET /prices/by-date?ticker=btc_usd&start_date=2026-10-15&end_date=2026-10-16
```

Параметры:
- `ticker` — тикер валюты.
- `start_date` — начало периода в формате `YYYY-MM-DD`.
- `end_date` — конец периода в формате `YYYY-MM-DD`.


## Design decisions

- **FastAPI** используется для создания REST API.
- **PostgreSQL** хранит историю цен.
- **SQLAlchemy** используется для работы с базой данных.
- **Celery и Celery Beat** отвечают за выполнение периодической задачи.
- **Redis** используется как брокер сообщений Celery.
- **Deribit Index Price API** используется для получения индексных цен BTC и ETH.
- **UNIX timestamp** хранится в базе данных как целое число.
- Обе валюты хранятся в одной таблице и различаются по полю `ticker`.