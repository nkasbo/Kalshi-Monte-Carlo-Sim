import requests
import os
from kalshi.api.client import KalshiClient
from kalshi.pricing.implied import implied_yes_prob
from kalshi.sim.monte_carlo import run_mc

MARKET_TICKER = "PUT_TICKER_HERE"
N_SIMULATIONS = 100_000


def main():
    client = KalshiClient()

    orderbook = client.get_orderbook(MARKET_TICKER)
    p_yes = implied_yes_prob(orderbook)

    probs = [p_yes, 1 - p_yes]
    counts, freqs = run_mc(probs, N_SIMULATIONS)

    print("\nGreenland Market Monte Carlo")
    print("----------------------------")
    print(f"YES probability: {p_yes:.4f}")
    print(f"NO probability:  {1 - p_yes:.4f}")
    print(f"Simulated YES freq: {freqs[0]:.4f}")
    print(f"Simulated NO freq:  {freqs[1]:.4f}")


if __name__ == "__main__":
    main()
