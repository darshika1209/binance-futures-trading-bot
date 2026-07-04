import hashlib
import hmac
import time
from typing import Any, Dict, Optional

import requests

from bot.logging_config import setup_logger

logger = setup_logger("binance_client")

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = TESTNET_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("BinanceClient initialised | Testnet: %s", self.base_url)

    def _sign(self, params: Dict) -> str:
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def _timestamp() -> int:
        return int(time.time() * 1000)

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        endpoint = "/fapi/v1/order"
        url = self.base_url + endpoint

        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": self._timestamp(),
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        params["signature"] = self._sign(params)

        logger.info(
            "Sending %s %s order | symbol=%s qty=%s price=%s",
            order_type, side, symbol, quantity, price or "MARKET",
        )
        logger.debug("Request params (no signature): %s",
                     {k: v for k, v in params.items() if k != "signature"})

        try:
            response = self.session.post(url, params=params, timeout=10)
            logger.debug("HTTP %s | Response: %s", response.status_code, response.text)
            response.raise_for_status()
            data = response.json()
            logger.info(
                "Order SUCCESS | orderId=%s status=%s executedQty=%s",
                data.get("orderId"), data.get("status"), data.get("executedQty"),
            )
            return data

        except requests.exceptions.ConnectionError as e:
            logger.error("Connection failed — testnet may be geo-restricted: %s", e)
            raise ConnectionError(
                "Cannot reach Binance Futures Testnet (testnet.binancefuture.com). "
                "This endpoint is geo-restricted in some regions (including India). "
                f"Original error: {e}"
            )
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error: %s | Body: %s", e, response.text)
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise TimeoutError("Binance Futures Testnet request timed out.")
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise
