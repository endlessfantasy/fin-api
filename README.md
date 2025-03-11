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
GET /fakestockdata?stock=AAPL&days=5&interval=1h
```

**Example Response:**
```json
{
  "stock": "AAPL",
  "interval": "1h",
  "data": [
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "current_price": 151.23,
      "change": 1.45,
      "change_percent": 0.97,
      "open": 150.50,
      "high": 152.00,
      "low": 149.80,
      "previous_close": 149.78,
      "volume": 5200000,
      "timestamp": "2024-03-01T10:30:00Z"
    },
    "news" : [
      {
        "date" : "January 15th",
        "headline" : "Mixed Economic Data Creates Uncertainty",
        "arcitle" : "Economic indicators present a mixed picture, leading to market volatility. Concerns about inflation persist despite positive jobs data. Experts suggest a cautious approach, recommending diversification across sectors."
      }
    ]
  ]
  }
```
Note: The time stamp does not contain the timezone

<br>

# TODO:
- Add error handling using pydantic
- Improve the news article generation