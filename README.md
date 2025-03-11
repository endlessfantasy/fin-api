# FastAPI Stock Data API

This is a FastAPI-based stock data API that retrieves stock information and historical stock data.

## Features
- Retrieve general stock information.
- Fetch historical stock data for a given stock symbol, time period, and interval.


## API Endpoints

### Root Endpoint
```http
GET /
```
**Response:**
```json
{
  "message": "API for Financial Rougelike Simulation by Team NexusCode",
  "status": "ACTIVE"
}
```


### Get Stock Historical Data
```http
GET /stock-data
```
**Query Parameters:**
- `stock` (string, required) - Stock ticker symbol (e.g., `AAPL`).
- `days` (integer, required) - Number of days of historical data.
- `interval` (string, optional) - Time interval (`1m`, `2m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1wk`, `1mo`). Default is `1d`.

**Example Request:**
```http
GET /stock-data?stock=AAPL&days=5&interval=1h
```

**Example Response:**
```json
{
  "stock": "AAPL",
  "interval": "1h",
  "data": [
    {
      "symbol": "AAPL",
      "company_name": "Test Inc.",
      "current_price": 145.3,
      "change": 2.1,
      "change_percent": 1.47,
      "open": 143.2,
      "high": 146.0,
      "low": 142.8,
      "previous_close": 143.2,
      "volume": 11234567,
      "timestamp": "2025-03-07T00:00:00-05:00Z"
    }
  ]
}
```

### Generate Fake Stock Historical Data
```http
GET /fakestockdata
```

**Query Parameters**:

- `symbol` (string, optional) - Stock ticker symbol (default: `TIC`).
- `company_name` (string, optional) - Company name (default: `Test Inc`).
- `start_price` (float, optional) - Starting stock price (default: `100.0`).
- `end_price` (float, optional) - Ending stock price (optional).
- `days` (integer, optional) - Number of days to generate data (default: `365`).
- `volatility` (float, optional) - Daily stock price volatility (default: `0.01`).
- `drift` (float, optional) - Expected drift in stock price (default: `0.0005`).
- `volume_mean` (integer, optional) - Average trading volume (default: `10,000,000`).
- `interval` (string, optional) - Time interval (`1m`, `2m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1wk`, `1mo`). Default is `1d`.
- `random_seed` (integer, optional) - Random seed for reproducibility.
- `start_date` (string, optional) - Start date for stock data in YYYY-MM-DD format (default: `2023-01-01`).


**Example Request:**
```http
GET fakestockdata?stock=AAPL&days=1&interval=1d
```

**Example Response:**
```json
{
  "stock": "AAPL",
  "interval": "1d",
  "data": [
    {
      "symbol": "AAPL",
      "company_name": "Test Inc",
      "current_price": 100.0,
      "change": 0.0,
      "change_percent": 0.0,
      "open": 99.94,
      "high": 100.11,
      "low": 99.41,
      "previous_close": 100.0,
      "volume": 9775082,
      "timestamp": "2023-01-01T00:00:00Z"
    }
  ],
  "news": [
    {
      "date": "January 15th",
      "headline": "Trading Volume Skyrockets Amidst Market Optimism",
      "article": "A surge in trading volume was observed today, fueled by positive sentiment surrounding upcoming earnings reports. Investors are eagerly anticipating the release of key financial data, leading to increased activity in the market. Some analysts are predicting a continuation of this trend as more companies announce their results in the coming weeks."
    },
    {
      "date": "February 22nd",
      "headline": "Market Holds Steady Despite Mixed Economic Data",
      "article": "The market remained relatively stable today, despite the release of mixed economic indicators. While consumer confidence showed signs of improvement, concerns linger regarding inflation and potential interest rate hikes. Experts suggest that investors are adopting a wait-and-see approach as they assess the overall economic outlook."
    }
  ]
}
```
Note: The time stamp does not contain the timezone

<br>

# TODO:
- Add error handling using pydantic
- Improve the news article generation
- High amount of data processing is causing timeout issues
- PLOTTING SO MUCH DATA THAT IT MAY NOT BE POSSIBLE TO SEE DETAILS (Candles, Ohlc-Bars, Etc.) AND TEXT MAY OVERLAP. Maybe use line chart instead.
