import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"


class KalshiClient:
    def __init__(self, timeout=20):
        self.base = BASE_URL
        self.timeout = timeout

    def _get(self, path, params=None):
        url = self.base + path
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # ---------- Public endpoints ----------

    def get_market(self, ticker):
        return self._get(f"/markets/{ticker}")

    def get_event(self, event_ticker):
        return self._get(f"/events/{event_ticker}")

    def get_event_markets(self, event_ticker):
        return self._get(f"/events/{event_ticker}/markets")

    def get_orderbook(self, ticker):
        return self._get(f"/markets/{ticker}/orderbook")