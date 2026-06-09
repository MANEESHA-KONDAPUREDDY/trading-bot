import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://demo-fapi.binance.com"


class BinanceClient:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(self, method: str, endpoint: str, params: dict = None, signed: bool = False):
        url = f"{self.base_url}{endpoint}"
        params = params or {}

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._sign(params)

        logger.info("REQUEST  %s %s | params=%s", method, endpoint, {k: v for k, v in params.items() if k != "signature"})

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method == "POST":
                response = self.session.post(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.info("RESPONSE %s | body=%s", response.status_code, response.text[:500])
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error: %s | response: %s", e, response.text)
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: %s", e)
            raise
        except requests.exceptions.Timeout as e:
            logger.error("Request timed out: %s", e)
            raise

    def get_server_time(self):
        return self._request("GET", "/fapi/v1/time")

    def get_exchange_info(self):
        return self._request("GET", "/fapi/v1/exchangeInfo")

    def place_order(self, **kwargs):
        return self._request("POST", "/fapi/v1/order", params=kwargs, signed=True)
