# Binance Futures Trading Bot (Demo/Testnet)

A Python CLI trading bot for Binance Futures Demo environment (USDT-M).  
Supports Market and Limit orders with structured logging and error handling.

---

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance REST API wrapper
    orders.py          # Order placement logic + output formatting
    validators.py      # Input validation
    logging_config.py  # File + console logging setup
  cli.py               # CLI entry point (argparse)
  .env.example         # API key template
  requirements.txt
  README.md
```

---

## Setup

### 1. Clone / download the project

```bash
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Get Demo API keys from: https://demo.binance.com/en/my/settings/api-management

Copy the template and fill in your keys:

```bash
copy .env.example .env
```

Edit `.env`:
```
BINANCE_API_KEY=your_demo_api_key_here
BINANCE_SECRET_KEY=your_demo_secret_key_here
```

> **Note:** These are Demo Trading keys — no real money is used.

---

## How to Run

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.1
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000
```

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

### Help

```bash
python cli.py --help
```

---

## Output Example

```
====================================================
  ORDER REQUEST SUMMARY
====================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
====================================================

====================================================
  ORDER RESPONSE
====================================================
  Order ID      : 123456789
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : FILLED
  Executed Qty  : 0.01
  Avg Price     : 62666.1
====================================================
  Order placed successfully!
====================================================
```

---

## Logs

All API requests, responses, and errors are saved to `logs/trading_bot_<timestamp>.log`.

---

## Assumptions

- Uses Binance Demo Futures API endpoint: `https://demo-fapi.binance.com`
- The original testnet URL (`testnet.binancefuture.com`) now redirects to Binance Demo Trading
- Demo API is functionally equivalent to the testnet — fake balance, real API calls
- `timeInForce=GTC` (Good Till Cancelled) is used for all Limit orders
