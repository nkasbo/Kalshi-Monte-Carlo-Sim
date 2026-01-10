import pandas as pd
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


def market_to_dataframe(market: Dict) -> pd.DataFrame:
    """Convert a market dictionary to a pandas DataFrame with a single row."""
    data = {
        "timestamp": datetime.now().isoformat(),
        "ticker": market.get("Ticker"),
        "title": market.get("Title"),
        "status": market.get("Status"),
        "closes": market.get("Closes"),
        "yes_bid": market.get("YES bid"),
        "yes_ask": market.get("YES ask"),
        "no_bid": market.get("NO bid"),
        "no_ask": market.get("NO ask"),
        "implied_p_yes": market.get("Implied P(YES)"),
        "volume_24h": market.get("24h Volume"),
        "open_interest": market.get("Open Interest"),
        "liquidity": market.get("Liquidity ($)")
    }
    return pd.DataFrame([data])


def save_market(market: Dict, filepath: str = "data/markets.csv", mode: str = "append") -> None:
    """
    Save market data to a CSV file.
    
    Args:
        market: Cleaned market dictionary (from clean_market())
        filepath: Path to CSV file (default: data/markets.csv)
        mode: 'append' to add to existing file, 'overwrite' to replace
    """
    # Convert market to DataFrame
    df = market_to_dataframe(market)
    
    # Create directory if it doesn't exist
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists
    file_exists = Path(filepath).exists()
    
    if mode == "append" and file_exists:
        # Append to existing file
        df.to_csv(filepath, mode='a', header=False, index=False)
    else:
        # Create new file or overwrite
        df.to_csv(filepath, mode='w', header=True, index=False)
    
    print(f"✓ Saved to {filepath}")


def load_markets(filepath: str = "data/markets.csv") -> Optional[pd.DataFrame]:
    """
    Load market data from CSV file.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        DataFrame with all market snapshots, or None if file doesn't exist
    """
    if not Path(filepath).exists():
        print(f"No data file found at {filepath}")
        return None
    
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def get_latest_snapshot(ticker: str, filepath: str = "data/markets.csv") -> Optional[Dict]:
    """
    Get the most recent snapshot for a specific ticker.
    
    Args:
        ticker: Market ticker symbol
        filepath: Path to CSV file
    
    Returns:
        Dictionary with latest market data, or None if not found
    """
    df = load_markets(filepath)
    if df is None:
        return None
    
    ticker_data = df[df['ticker'] == ticker]
    if ticker_data.empty:
        return None
    
    # Get most recent entry
    latest = ticker_data.sort_values('timestamp', ascending=False).iloc[0]
    return latest.to_dict()
