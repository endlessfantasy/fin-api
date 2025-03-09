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
  "message": "Hello World"
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
GET /stock-data/?stock=AAPL&days=5&interval=1h
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
      "current_price": 145.3,
      "change": 2.1,
      "change_percent": 1.47,
      "open": 143.2,
      "high": 146.0,
      "low": 142.8,
      "previous_close": 143.2,
      "volume": 11234567,
      "timestamp": "2024-03-08T14:00:00Z"
    }
  ]
}
```

### Generate Fake Stock Historical Data
```http
GET /fakestockdata
```
