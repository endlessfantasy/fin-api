
import io
import json
import os
from typing import Dict, List, Optional

import mplfinance as mpf
import numpy as np
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv(".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


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
            return {
                "error": "No data found. Check the stock symbol or try again later."
            }

        # Convert stock data into the required format
        stock_data = []
        for index, row in history.iterrows():
            timestamp = index.to_pydatetime().isoformat() + "Z"
            stock_data.append(
                {
                    "symbol": symbol.upper(),
                    "company_name": info.get("shortName", "Unknown"),
                    "current_price": round(row["Close"], 2),
                    "change": round(row["Close"] - row["Open"], 2),
                    "change_percent": (
                        round(((row["Close"] - row["Open"]) / row["Open"]) * 100, 2)
                        if row["Open"]
                        else 0
                    ),
                    "open": round(row["Open"], 2),
                    "high": round(row["High"], 2),
                    "low": round(row["Low"], 2),
                    "previous_close": round(info.get("previousClose", row["Close"]), 2),
                    "volume": int(row["Volume"]),
                    "timestamp": timestamp,
                }
            )

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
        "1m": "T",
        "2m": "2T",
        "5m": "5T",
        "15m": "15T",
        "30m": "30T",
        "1h": "H",
        "1d": "D",
        "1wk": "W",
        "1mo": "MS",
    }

    if random_seed is not None:
        np.random.seed(random_seed)

    if interval not in INTERVAL_MAP:
        raise ValueError(
            f"Invalid interval '{interval}'. Choose from {list(INTERVAL_MAP.keys())}"
        )

    # Calculate the total number of intervals based on the interval and days
    if interval.endswith("m"):
        minutes = int(interval[:-1])
        intervals_per_day = 24 * 60 // minutes
    elif interval.endswith("h"):
        hours = int(interval[:-1])
        intervals_per_day = 24 // hours
    elif interval.endswith("d"):
        intervals_per_day = 1
    elif interval.endswith("wk"):
        intervals_per_day = 1 / 7
    elif interval.endswith("mo"):
        intervals_per_day = 1 / 30  # Approximation
    else:
        raise ValueError(f"Unsupported interval: {interval}")

    total_intervals = int(days * intervals_per_day)

    freq = INTERVAL_MAP[interval]
    date_range = pd.date_range(start=start_date, periods=total_intervals, freq=freq)
    stock_prices = np.zeros(total_intervals)
    stock_prices[0] = start_price

    if end_price:
        drift = (end_price / start_price) ** (1 / total_intervals) - 1  # Adjust drift

    for i in range(1, total_intervals):
        daily_return = np.random.normal(drift, volatility)
        stock_prices[i] = stock_prices[i - 1] * (1 + daily_return)

    if turning_points:
        for day, price in turning_points.items():
            if 0 <= day < total_intervals:
                stock_prices[day] = price

    data = []
    for i in range(total_intervals):
        open_price = stock_prices[i] * (1 + np.random.uniform(-0.005, 0.005))
        high_price = open_price * (1 + np.random.uniform(0.001, 0.01))
        low_price = open_price * (1 - np.random.uniform(0.001, 0.01))
        close_price = stock_prices[i]
        previous_close = stock_prices[i - 1] if i > 0 else start_price
        change = close_price - previous_close
        change_percent = (change / previous_close) * 100
        volume = int(np.random.normal(volume_mean, volume_mean * 0.1))
        timestamp = date_range[i].strftime("%Y-%m-%dT%H:%M:%SZ")  # No timezone

        data.append(
            {
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
            }
        )

    return data


def plot_candlestick_chart_and_get_image_data(
    stock_data: str, symbol: str = "TEST", currency: str = "RS"
) -> Image.Image:
    """Plots stock price as a candlestick chart, saves it to memory, and returns PIL.Image object."""
    df = pd.DataFrame(stock_data)
    df.set_index("timestamp", inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[["open", "high", "low", "current_price", "volume"]]
    df.rename(columns={"current_price": "close"}, inplace=True)

    # Custom style with larger figure size and better visibility
    fig, axlist = mpf.plot(
        df,
        type="candle",
        style="charles",
        title=f"{symbol} Candlestick Chart",
        ylabel=f"Price ({currency})",
        volume=True,
        figsize=(12, 8),
        returnfig=True,
    )

    # Increase font size
    for ax in axlist:
        ax.title.set_size(16)
        ax.xaxis.label.set_size(14)
        ax.yaxis.label.set_size(14)
        ax.tick_params(axis="both", labelsize=12)

    # Save the figure to a memory buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    image = Image.open(buf)
    return image


async def get_news(image: Image.Image) -> Dict[str, List[Dict[str, str]]]:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["response"],
            properties = {
                "response": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["date", "headline", "article"],
                        properties = {
                            "date": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "headline": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "article": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        },
                    ),
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text="""You are an ai assisstant that generates news articles from images of financial trends in following json format.
The articles should be of at least 3 lines. Generate some events that hints at the future stock prices.
Do not directly say the stock is going up or down. Do not reference the candlestick in the news articles.

```json
{
  {
    'date' : 'January 15th',
    'headline' : `,
    'article' : ' ' 
  }
}
``` """),
        ],
    )
    
    content = "Generate some news articles for each month in the picture along with their headlines from the image that can be used to predict the the trends in the data. It will be sent to a player and they would need to predict the outcome. Give the news articles at different points of time."

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[content, image],
        config=generate_content_config
    )
    return (json.loads(response.text))
