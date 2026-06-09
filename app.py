import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from bot.client import BinanceClient
from bot.logging_config import setup_logging
from bot.orders import place_limit_order, place_market_order, place_stop_limit_order
from bot.validators import validate_inputs

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)
app = Flask(__name__)

order_history = []


def get_client():
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    secret_key = os.getenv("BINANCE_SECRET_KEY", "").strip()
    if not api_key or not secret_key:
        raise ValueError("API keys not configured. Set BINANCE_API_KEY and BINANCE_SECRET_KEY.")
    return BinanceClient(api_key, secret_key)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json()

    symbol = data.get("symbol", "")
    side = data.get("side", "")
    order_type = data.get("order_type", "")
    quantity = data.get("quantity")
    price = data.get("price") or None
    stop_price = data.get("stop_price") or None

    try:
        symbol, side, order_type, quantity, price, stop_price = validate_inputs(
            symbol, side, order_type, quantity, price, stop_price
        )
    except ValueError as e:
        logger.warning("Validation error: %s", e)
        return jsonify({"success": False, "error": str(e)}), 400

    try:
        client = get_client()

        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price)
        else:
            response = place_stop_limit_order(client, symbol, side, quantity, price, stop_price)

        order_record = {
            "orderId": response.get("orderId"),
            "symbol": response.get("symbol"),
            "side": response.get("side"),
            "type": response.get("type"),
            "status": response.get("status"),
            "quantity": response.get("origQty"),
            "executedQty": response.get("executedQty"),
            "price": response.get("avgPrice") or response.get("price") or "—",
        }
        order_history.insert(0, order_record)

        return jsonify({"success": True, "order": order_record})

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        logger.error("Order failed: %s", e, exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(order_history)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
