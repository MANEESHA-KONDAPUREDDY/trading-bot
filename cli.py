import argparse
import os
import sys

from dotenv import load_dotenv

from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.validators import validate_inputs
from bot.orders import (
    place_limit_order,
    place_market_order,
    place_stop_limit_order,
    print_order_response,
    print_order_summary,
)

load_dotenv()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Demo Futures Trading Bot (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", required=True, dest="order_type", choices=["MARKET", "LIMIT", "STOP_LIMIT"],
        help="Order type: MARKET, LIMIT, or STOP_LIMIT"
    )
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument(
        "--price", type=float, default=None,
        help="Limit price in USDT (required for LIMIT and STOP_LIMIT orders)"
    )
    parser.add_argument(
        "--stop-price", type=float, default=None, dest="stop_price",
        help="Stop trigger price in USDT (required for STOP_LIMIT orders)"
    )
    return parser


def main():
    log_file = setup_logging()

    import logging
    logger = logging.getLogger(__name__)
    logger.info("Trading bot started | log_file=%s", log_file)

    parser = build_parser()
    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    secret_key = os.getenv("BINANCE_SECRET_KEY", "").strip()

    if not api_key or not secret_key:
        print("[ERROR] BINANCE_API_KEY and BINANCE_SECRET_KEY must be set in your .env file.")
        print("  Copy .env.example to .env and fill in your Demo API credentials.")
        sys.exit(1)

    try:
        symbol, side, order_type, quantity, price, stop_price = validate_inputs(
            args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price
        )
    except ValueError as e:
        print(f"[VALIDATION ERROR] {e}")
        logger.error("Validation failed: %s", e)
        sys.exit(1)

    print_order_summary(symbol, side, order_type, quantity, price, stop_price)

    client = BinanceClient(api_key, secret_key)

    try:
        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price)
        else:
            response = place_stop_limit_order(client, symbol, side, quantity, price, stop_price)

        print_order_response(response)

    except Exception as e:
        print(f"\n[ORDER FAILED] {e}")
        logger.error("Order placement failed: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
