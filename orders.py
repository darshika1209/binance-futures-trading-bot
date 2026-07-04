from typing import Any, Dict, Optional

from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger("orders")


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    logger.info("=" * 60)
    logger.info("NEW ORDER | %s %s %s | qty=%s | price=%s",
                order_type, side, symbol, quantity, price or "MARKET")
    logger.info("=" * 60)

    result = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )
    return result


def format_response(response: Dict[str, Any]) -> str:
    sep = "=" * 50
    lines = [
        f"\n{sep}",
        "  ORDER RESPONSE",
        sep,
        f"  Order ID     : {response.get('orderId', 'N/A')}",
        f"  Symbol       : {response.get('symbol', 'N/A')}",
        f"  Side         : {response.get('side', 'N/A')}",
        f"  Type         : {response.get('type', 'N/A')}",
        f"  Status       : {response.get('status', 'N/A')}",
        f"  Executed Qty : {response.get('executedQty', 'N/A')}",
        f"  Avg Price    : {response.get('avgPrice', 'N/A')}",
        f"  Update Time  : {response.get('updateTime', 'N/A')}",
        sep,
    ]
    return "\n".join(lines)
