# Stock Market Data Pipeline

Automated ETL pipeline for collecting and storing stock market data from Alpha Vantage API with PostgreSQL database.

## 📋 About

This project implements a complete ETL pipeline that:
- **Extracts** real-time stock market data from Alpha Vantage API
- **Transforms** raw data into structured format with validation
- **Loads** processed data into PostgreSQL database and CSV files

## 🚀 Technologies

- Python 3.8+
- PostgreSQL (database)
- Docker (containerization)
- Requests (HTTP client)
- Pandas (data manipulation)
- Schedule (task automation)
- Psycopg2 (PostgreSQL adapter)
- Alpha Vantage API (financial data)

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/michaelclaudino7/stock-data-pipeline.git
cd stock-data-pipeline

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🐳 Database Setup

**Start PostgreSQL with Docker:**
```bash
docker run --name stock-postgres \
  -e POSTGRES_USER=stockuser \
  -e POSTGRES_PASSWORD=stockpass \
  -e POSTGRES_DB=stock_market \
  -p 5432:5432 \
  -d postgres:15
```

**Create tables:**
```bash
docker exec -it stock-postgres psql -U stockuser -d stock_market
```
```sql
CREATE TABLE stocks (
    symbol VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) REFERENCES stocks(symbol),
    timestamp TIMESTAMP NOT NULL,
    price DECIMAL(10,2),
    volume BIGINT,
    latest_trading_day DATE,
    previous_close DECIMAL(10,2),
    change DECIMAL(10,2),
    change_percent DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_stock_prices_symbol ON stock_prices(symbol);
CREATE INDEX idx_stock_prices_timestamp ON stock_prices(timestamp);
```

## ⚙️ Configuration

1. Get a free API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Add your configuration in `.env`:
```
ALPHA_VANTAGE_API_KEY=your_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_market
DB_USER=stockuser
DB_PASSWORD=stockpass
```

## 🎯 Usage

**Run once:**
```bash
python3 run_pipeline.py
```

**Run automatically (daily at 18:00):**
```bash
python3 scheduler.py
```

## 📁 Project Structure
```
stock-data-pipeline/
├── data/
│   └── stock_data_YYYYMMDD.csv  # CSV backup
├── logs/
│   └── pipeline.log              # Execution logs
├── src/
│   ├── pipeline.py               # Main ETL pipeline
│   ├── database.py               # PostgreSQL connection
│   ├── config.py                 # Configuration
│   ├── data_validator.py         # Data validation
│   └── utils.py                  # Utility functions
├── run_pipeline.py               # Manual execution
├── scheduler.py                  # Automated execution
└── requirements.txt              # Dependencies
```

## 📊 Database Schema

**stocks** (dimension table)
- symbol (PK)
- name
- created_at

**stock_prices** (fact table)
- id (PK)
- symbol (FK)
- timestamp
- price
- volume
- latest_trading_day
- previous_close
- change
- change_percent
- created_at

## 📈 Query Examples
```sql
-- Latest prices
SELECT symbol, price, change_percent, timestamp 
FROM stock_prices 
ORDER BY timestamp DESC LIMIT 10;

-- Average price by stock
SELECT symbol, AVG(price) as avg_price 
FROM stock_prices 
GROUP BY symbol;

-- Daily volatility
SELECT DATE(timestamp), symbol, 
       MAX(price) - MIN(price) as daily_range
FROM stock_prices 
GROUP BY DATE(timestamp), symbol;
```

## 🔧 Customization

Edit `src/config.py` to monitor different stocks:
```python
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
```