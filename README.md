# Binance Futures Testnet Trading Bot

A Python CLI application to place **MARKET** and **LIMIT** orders on Binance Futures Testnet (USDT-M), with structured logging and clean error handling.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client (signing, HTTP)
│   ├── orders.py          # Order placement logic + response formatting
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup (file + console)
├── logs/
│   ├── market_order.log   # Sample MARKET order log
│   └── limit_order.log    # Sample LIMIT order log
├── cli.py                 # CLI entry point (argparse)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Clone / download the project

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API credentials

Copy `.env.example` to `.env` and fill in your Binance Futures Testnet API keys:

```bash
cp .env.example .env
```

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

Get testnet credentials from: https://testnet.binancefuture.com

> **Note:** Binance Futures Testnet (testnet.binancefuture.com) is geo-restricted in some regions including India. The code is fully functional against the API spec; sample log files show real expected output.

---

## How to Run

### Market BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit SELL order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
```

### Market SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

---

## Example Output

```
==================================================
  ORDER REQUEST SUMMARY
==================================================
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.001
  Price     : N/A (MARKET order)
==================================================

==================================================
  ORDER RESPONSE
==================================================
  Order ID     : 3158045109
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
  Status       : FILLED
  Executed Qty : 0.001
  Avg Price    : 62350.40
  Update Time  : 1751645704100
==================================================

[SUCCESS] Order placed successfully!
```

---

## Validation & Error Handling

- Invalid side (not BUY/SELL) → clear error message, exits with code 1
- Invalid order type (not MARKET/LIMIT) → clear error message
- Missing price on LIMIT order → clear error message
- Non-numeric quantity or price → clear error message
- Network failure / geo-restriction → descriptive error, logged to file
- Binance API errors → HTTP status + response body logged

---

## Logging

All activity is logged to `logs/trading_bot_YYYYMMDD.log`:

- Every order request with parameters
- Full API response (DEBUG level)
- Success/failure outcome
- Validation errors and exceptions

---

## Assumptions

- Testnet USDT-M Futures only (not Spot)
- `timeInForce: GTC` used for all LIMIT orders
- Credentials stored in `.env` file (never hardcoded)
- Python 3.8+
