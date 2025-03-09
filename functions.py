import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List
import numpy as np

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


async def generate_stock_data(
    symbol: str,
    company_name: str,
    start_price: float,
    end_price: Optional[float],
    days: int,
    volatility: float,
    drift: float,
    volume_mean: int,
    interval: str,
    random_seed: Optional[int],
    turning_points: Optional[Dict[int, float]],
    start_date: str,
) -> List[Dict]:
    """Generates synthetic stock price data asynchronously."""

    INTERVAL_MAP = {
    "1m": "T", "2m": "2T", "5m": "5T", "15m": "15T", "30m": "30T", 
    "1h": "H", "1d": "D", "1wk": "W", "1mo": "MS"
    }

    if random_seed is not None:
        np.random.seed(random_seed)
    
    if interval not in INTERVAL_MAP:
        raise ValueError(f"Invalid interval '{interval}'. Choose from {list(INTERVAL_MAP.keys())}")
    
    freq = INTERVAL_MAP[interval]
    date_range = pd.date_range(start=start_date, periods=days, freq=freq)
    stock_prices = np.zeros(days)
    stock_prices[0] = start_price
    
    if end_price:
        drift = (end_price / start_price) ** (1 / days) - 1  # Adjust drift
    
    for i in range(1, days):
        daily_return = np.random.normal(drift, volatility)
        stock_prices[i] = stock_prices[i - 1] * (1 + daily_return)
    
    if turning_points:
        for day, price in turning_points.items():
            if 0 <= day < days:
                stock_prices[day] = price
    
    data = []
    for i in range(days):
        open_price = stock_prices[i] * (1 + np.random.uniform(-0.005, 0.005))
        high_price = open_price * (1 + np.random.uniform(0.001, 0.01))
        low_price = open_price * (1 - np.random.uniform(0.001, 0.01))
        close_price = stock_prices[i]
        previous_close = stock_prices[i - 1] if i > 0 else start_price
        change = close_price - previous_close
        change_percent = (change / previous_close) * 100
        volume = int(np.random.normal(volume_mean, volume_mean * 0.1))
        timestamp = date_range[i].strftime("%Y-%m-%dT%H:%M:%SZ") # no timezone

        data.append({
            "symbol": symbol,
            "company_name": company_name,
            "current_price": round(close_price, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "previous_close": round(previous_close, 2),
            "volume": volume,
            "timestamp": timestamp,
        })
    
    return data