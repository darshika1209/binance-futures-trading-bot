import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import format_response, place_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

load_dotenv()
logger = setup_logger("cli")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  Limit SELL:
    python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
        """,
    )
    parser.add_argument("--symbol",   required=True,          help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True,          help="BUY or SELL")
    parser.add_argument("--type",     required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True,          help="Order quantity")
    parser.add_argument("--price",    required=False, default=None, help="Limit price (required for LIMIT orders)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logger.info("CLI invoked | symbol=%s side=%s type=%s qty=%s price=%s",
                args.symbol, args.side, args.order_type, args.quantity, args.price)

    # ── Validate ────────────────────────────────────────────────────────────
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity   = validate_quantity(args.quantity)
        price      = validate_price(args.price, order_type)
    except ValueError as e:
        logger.error("Validation failed: %s", e)
        print(f"\n[VALIDATION ERROR] {e}")
        sys.exit(1)

    # ── Print request summary ────────────────────────────────────────────────
    sep = "=" * 50
    print(f"\n{sep}")
    print("  ORDER REQUEST SUMMARY")
    print(sep)
    print(f"  Symbol    : {symbol}")
    print(f"  Side      : {side}")
    print(f"  Type      : {order_type}")
    print(f"  Quantity  : {quantity}")
    print(f"  Price     : {price if price else 'N/A (MARKET order)'}")
    print(sep)

    # ── Load credentials ─────────────────────────────────────────────────────
    api_key    = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")

    if not api_key or not api_secret:
        print("\n[ERROR] API credentials not found.")
        print("Create a .env file with BINANCE_API_KEY and BINANCE_API_SECRET.")
        sys.exit(1)

    # ── Place order ──────────────────────────────────────────────────────────
    client = BinanceClient(api_key=api_key, api_secret=api_secret)

    try:
        response = place_order(client, symbol, side, order_type, quantity, price)
        print(format_response(response))
        print("\n[SUCCESS] Order placed successfully!\n")
        logger.info("Order flow completed successfully.")

    except ConnectionError as e:
        print(f"\n[CONNECTION ERROR] {e}")
        logger.error("Connection error: %s", e)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        logger.error("Unexpected error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
