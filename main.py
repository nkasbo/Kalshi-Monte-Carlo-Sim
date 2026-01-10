from typing import Dict
from src.kalshi.api.client import KalshiClient
from src.kalshi.data.storage import save_market


def clean_market(market: Dict) -> Dict:
    """Extracts and formats only the important, readable fields."""
    yes_bid = market.get("yes_bid")
    yes_ask = market.get("yes_ask")

    p_yes = None
    if yes_bid is not None and yes_ask is not None:
        p_yes = round(((yes_bid + yes_ask) / 2) / 100, 4)

    return {
        "Ticker": market.get("ticker"),
        "Title": market.get("title"),
        "Status": market.get("status"),
        "Closes": market.get("close_time"),
        "YES bid": yes_bid,
        "YES ask": yes_ask,
        "NO bid": market.get("no_bid"),
        "NO ask": market.get("no_ask"),
        "Implied P(YES)": p_yes,
        "24h Volume": market.get("volume_24h"),
        "Open Interest": market.get("open_interest"),
        "Liquidity ($)": market.get("liquidity_dollars"),
    }


def main():
    print("Kalshi Monte Carlo Simulator\n")

    ticker = input("Enter Market Ticker (e.g. KXGREENTERRITORY-29): ").strip().upper()

    client = KalshiClient()

    
    # Try to get as a market first
    try:
        market = client.get_market(ticker)
        cleaned = clean_market(market)
        
        print("\nMarket Summary")
        print("-" * 40)
        for k, v in cleaned.items():
            print(f"{k:20}: {v}")
        
        # Ask to save
        print("\n" + "-" * 40)
        save_choice = input("Save to CSV? (y/n): ").strip().lower()
        if save_choice == 'y':
            save_market(cleaned)
            
    except Exception as e:
        if "404" in str(e):
            # Might be an event - try the full ticker first, then stripped version
            print(f"\n'{ticker}' not found as a market. Trying as event...")
            
            # Try full ticker first
            event_tickers_to_try = [ticker]
            # Also try without suffix (e.g., KXUCLFINALIST-26 -> KXUCLFINALIST)
            if '-' in ticker:
                event_tickers_to_try.append(ticker.rsplit('-', 1)[0])
            
            for event_ticker in event_tickers_to_try:
                try:
                    # Try using search_markets with event_ticker parameter
                    markets = client.search_markets(query=event_ticker, limit=100)
                    
                    if not markets:
                        continue
                        
                    print(f"\nFound {len(markets)} markets for event '{event_ticker}':")
                    print("-" * 60)
                    for i, market in enumerate(markets, 1):
                        print(f"\n{i}. {market.get('ticker')}")
                        print(f"   {market.get('title')}")
                    return
                    
                except Exception:
                    continue
            
            print(f"\nError: Could not find '{ticker}' as a market or event")
        else:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
