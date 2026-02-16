# Stock Market Data Pipeline

Automated ETL pipeline for collecting and storing stock market data from Alpha Vantage API.

## 📋 About

This project implements a complete ETL pipeline that:
- **Extracts** real-time stock market data from Alpha Vantage API
- **Transforms** raw data into structured format with validation
- **Loads** processed data into CSV files for analysis

## 🚀 Technologies

- Python 3.8+
- Requests (HTTP client)
- Pandas (data manipulation)
- Schedule (task automation)
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

## ⚙️ Configuration

1. Get a free API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Add your API key in `.env`:
```
ALPHA_VANTAGE_API_KEY=your_key_here
```

## 🎯 Usage

**Run once:**
```bash
python run_pipeline.py
```

**Run automatically (every hour):**
```bash
python scheduler.py
```

## 📁 Project Structure
```
stock-data-pipeline/
├── data/
│   ├── stock_data_YYYYMMDD.csv  # Daily data
│   └── stock_data_history.csv   # Complete history
├── logs/
│   └── pipeline.log              # Execution logs
├── src/
│   ├── pipeline.py               # Main ETL pipeline
│   ├── config.py                 # Configuration
│   ├── data_validator.py         # Data validation
│   └── utils.py                  # Utility functions
├── run_pipeline.py               # Manual execution
├── scheduler.py                  # Automated execution
└── requirements.txt              # Dependencies
```

## 📊 Collected Data

For each stock (AAPL, TSLA by default):
- Current price (USD)
- Trading volume
- Price change (value and %)
- Previous close price
- Latest trading day
- Collection timestamp

## 🔧 Customization

Edit `src/config.py` to monitor different stocks:
```python
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
```