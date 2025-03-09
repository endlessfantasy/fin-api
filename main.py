from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions import get_stock_info, get_stock_data, generate_stock_data

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["GET"], 
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/stock/{symbol}")
async def get_info(symbol: str):
    return get_stock_info(symbol)

@app.get("/stock-data")
async def get_data(stock: str, days: int, interval: str = "1d"):
    return get_stock_data(stock, days, interval)

@app.get("/fakestockdata")
async def get_fake_data(
    symbol: str = "TIC",
    company_name: str = "Test Inc",
    start_price: float = 100.0,
    end_price: float = None,
    days: int = 365,
    volatility: float = 0.01,
    drift: float = 0.0005,
    volume_mean: int = 10000000,
    interval: str = "1d",
    random_seed: int = None,
    start_date: str = "2023-01-01"
):
    turning_points = None  # GET requests cannot send a JSON body directly
    
    fake_data = await generate_stock_data(symbol, company_name, start_price, end_price, days, 
                                    volatility, drift, volume_mean, interval, 
                                    random_seed, turning_points, start_date)
    return {"stock": symbol, "interval": interval, "data": fake_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
