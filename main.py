from src.kalshi.api.client import KalshiClient

def main():
    print("Hello from kalshi-monte-carlo-simulator!")
    Ticker = input("Please enter the Market Ticker: ")
    run1 = KalshiClient()
    datadump = run1.get_event(Ticker)
    print(datadump)


if __name__ == "__main__":
    main()
