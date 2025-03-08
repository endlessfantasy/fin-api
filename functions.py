import yfinance as yf
import pandas as pd
def get_stock_info(symbol: str):
    try:
        response = yf.Ticker(symbol)
        return response.info
    except Exception as e:
        return {"error": "INVALID SYMBOL"}


def get_stock_data(symbol: str, days: int = 1, interval: str = "1d"):
    """
    Fetch stock data for a given stock symbol, time period, and interval.
    Example query: /stock-data/?symbol=AAPL&days=5&interval=1h
    """
    try:
        # Validate interval
        valid_intervals = ["1m", "2m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"]
        if interval not in valid_intervals:
            return {"error": f"Invalid interval. Choose from {valid_intervals}"}

        # Fetch stock data
        stock = yf.Ticker(symbol)
        info = stock.info  # General company info
        history = stock.history(period=f"{days}d", interval=interval)

        # Ensure data is available
        if history.empty:
            return {"error": "No data found. Check the stock symbol or try again later."}

        # Convert stock data into the required format
        stock_data = []
        for index, row in history.iterrows():
            timestamp = index.to_pydatetime().isoformat() + "Z"
            stock_data.append({
                "symbol": symbol.upper(),
                "company_name": info.get("shortName", "Unknown"),
                "current_price": round(row["Close"], 2),
                "change": round(row["Close"] - row["Open"], 2),
                "change_percent": round(((row["Close"] - row["Open"]) / row["Open"]) * 100, 2) if row["Open"] else 0,
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "previous_close": round(info.get("previousClose", row["Close"]), 2),
                "volume": int(row["Volume"]),
                "timestamp": timestamp
            })

        return {"stock": symbol.upper(), "interval": interval, "data": stock_data}

    except Exception as e:
        return {"error": "INVALID REQUEST. CHECK TRADING SYMBOL"}
