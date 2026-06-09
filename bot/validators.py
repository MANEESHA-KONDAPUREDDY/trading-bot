import logging

logger = logging.getLogger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}


def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    if not symbol.isalnum():
        raise ValueError(f"Invalid symbol '{symbol}'. Use alphanumeric only (e.g. BTCUSDT).")
    return symbol


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {sorted(VALID_SIDES)}.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {sorted(VALID_ORDER_TYPES)}.")
    return order_type


def validate_quantity(quantity) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {qty}.")
    return qty


def validate_price(price) -> float:
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid price '{price}'. Must be a positive number.")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0, got {p}.")
    return p


def validate_inputs(symbol, side, order_type, quantity, price=None, stop_price=None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders. Use --price.")
        price = validate_price(price)

    if order_type == "STOP_LIMIT":
        if price is None:
            raise ValueError("Price (limit price) is required for STOP_LIMIT orders.")
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders. Use --stop-price.")
        price = validate_price(price)
        stop_price = validate_price(stop_price)

    logger.debug(
        "Validated inputs: symbol=%s side=%s type=%s qty=%s price=%s stop_price=%s",
        symbol, side, order_type, quantity, price, stop_price,
    )
    return symbol, side, order_type, quantity, price, stop_price
