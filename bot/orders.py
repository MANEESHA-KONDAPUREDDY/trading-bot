import logging

from bot.client import BinanceClient

logger = logging.getLogger(__name__)


def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: float) -> dict:
    logger.info("Placing MARKET order | symbol=%s side=%s qty=%s", symbol, side, quantity)
    return client.place_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity,
    )


def place_limit_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, price: float
) -> dict:
    logger.info(
        "Placing LIMIT order | symbol=%s side=%s qty=%s price=%s",
        symbol, side, quantity, price,
    )
    return client.place_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=quantity,
        price=price,
        timeInForce="GTC",
    )


def place_stop_limit_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, price: float, stop_price: float
) -> dict:
    logger.info(
        "Placing STOP_LIMIT order | symbol=%s side=%s qty=%s price=%s stopPrice=%s",
        symbol, side, quantity, price, stop_price,
    )
    return client.place_order(
        symbol=symbol,
        side=side,
        type="STOP",
        quantity=quantity,
        price=price,
        stopPrice=stop_price,
        timeInForce="GTC",
    )


def print_order_summary(symbol: str, side: str, order_type: str, quantity: float, price=None, stop_price=None):
    print("\n" + "=" * 52)
    print("  ORDER REQUEST SUMMARY")
    print("=" * 52)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price} USDT")
    if stop_price is not None:
        print(f"  Stop Price : {stop_price} USDT")
    print("=" * 52)


def print_order_response(response: dict):
    print("\n" + "=" * 52)
    print("  ORDER RESPONSE")
    print("=" * 52)
    print(f"  Order ID      : {response.get('orderId', 'N/A')}")
    print(f"  Client OID    : {response.get('clientOrderId', 'N/A')}")
    print(f"  Symbol        : {response.get('symbol', 'N/A')}")
    print(f"  Side          : {response.get('side', 'N/A')}")
    print(f"  Type          : {response.get('type', 'N/A')}")
    print(f"  Status        : {response.get('status', 'N/A')}")
    print(f"  Executed Qty  : {response.get('executedQty', 'N/A')}")
    avg_price = response.get('avgPrice') or response.get('price', 'N/A')
    print(f"  Avg Price     : {avg_price}")
    print("=" * 52)
    print("  Order placed successfully!")
    print("=" * 52 + "\n")
    logger.info("Order placed successfully | orderId=%s status=%s", response.get('orderId'), response.get('status'))
