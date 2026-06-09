# TradingBot Pro — Binance Futures Demo

A Python trading bot for Binance Futures Demo (USDT-M) with a professional Web UI and CLI interface.  
Supports Market, Limit, and Stop-Limit orders with real-time TradingView charts, structured logging, and full error handling.

---

## Live Demo

**Web UI:** https://tradingbot-rosy.vercel.app  
**GitHub:** https://github.com/MANEESHA-KONDAPUREDDY/trading-bot

---

## Features

- Place **Market**, **Limit**, and **Stop-Limit** orders
- Support for both **BUY** and **SELL** sides
- Professional **Web UI** (Binance-style dark theme)
- **TradingView live chart** with timeframe switching
- **CLI interface** via argparse
- **Mobile responsive** — bottom tab navigation
- **Field-level validation** with inline error messages
- **Structured logging** to file (local) and console
- **Error handling** for API errors, network failures, invalid input

---

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance REST API wrapper + request signing
    orders.py          # Order placement logic + output formatting
    validators.py      # Input validation for all order types
    logging_config.py  # Logging setup (file + console)
  templates/
    index.html         # Web UI (Flask template)
  app.py               # Flask web application
  cli.py               # CLI entry point (argparse)
  .env.example         # API key template
  requirements.txt
  Procfile
  vercel.json
  README.md
```

---

## Setup — Run Locally

### Step 1 — Get Demo API Keys

1. Go to **demo.binance.com** and log in (Google login works)
2. Navigate to: **Profile → API Management**
3. Click **"Create API"**, enter label: `trading_bot`
4. Copy your **API Key** and **Secret Key** (Secret shown only once!)

> **Note:** These are Demo Trading keys — no real money is used.

---

### Step 2 — Clone the Repository

```bash
git clone https://github.com/MANEESHA-KONDAPUREDDY/trading-bot.git
cd trading-bot
```

---

### Step 3 — Create Virtual Environment

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Configure API Keys

Copy the example env file and add your keys:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` file:
```
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_SECRET_KEY=your_actual_secret_key_here
```

> Keys must be from **demo.binance.com → API Management**  
> Do NOT add any extra text — just the key itself.

---

### Step 6 — Run the Web UI

```bash
python app.py
```

Open browser: **http://localhost:5000**

---

### Step 7 — Run via CLI

**Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

**Stop-Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.001 --price 62000 --stop-price 63000
```

**Help:**
```bash
python cli.py --help
```

---

## CLI Output Example

```
====================================================
  ORDER REQUEST SUMMARY
====================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
====================================================

====================================================
  ORDER RESPONSE
====================================================
  Order ID      : 14559997364
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : NEW
  Executed Qty  : 0.001
  Avg Price     : 62666.10
====================================================
  Order placed successfully!
====================================================
```

---

## Logs

All API requests, responses, and errors are saved to:
```
logs/trading_bot_YYYYMMDD_HHMMSS.log
```

---

## API Endpoints (Web UI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| POST | `/api/order` | Place an order |
| GET | `/api/orders` | Get order history |

---

## Assumptions

- Uses **Binance Demo Futures API**: `https://demo-fapi.binance.com`
- The original testnet URL (`testnet.binancefuture.com`) now redirects to Binance Demo Trading (`demo.binance.com`)
- Demo API is functionally equivalent to the testnet — fake balance, real API structure
- `timeInForce=GTC` (Good Till Cancelled) is used for Limit and Stop-Limit orders
- Order history is stored in-memory (resets on server restart)
- Vercel deployment uses Mumbai region (`bom1`) to avoid Binance geo-restrictions

---

## Requirements

```
requests==2.31.0
python-dotenv==1.0.1
flask==3.0.3
```
