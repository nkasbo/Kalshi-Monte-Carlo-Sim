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
        response = self._get(f"/markets/{ticker}")
        return response.get("market", response)

    def get_event(self, event_ticker):
        response = self._get(f"/events/{event_ticker}")
        return response.get("event", response)

    def get_event_markets(self, event_ticker):
        return self._get(f"/events/{event_ticker}/markets")

    def get_orderbook(self, ticker):
        return self._get(f"/markets/{ticker}/orderbook")

    def search_markets(self, query=None, limit=20, status="open"):
        """Search for markets. Returns list of markets."""
        params = {"limit": limit, "status": status}
        if query:
            params["event_ticker"] = query
        response = self._get("/markets", params=params)
        return response.get("markets", [])