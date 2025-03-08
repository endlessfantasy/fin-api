from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions import get_stock_info, get_stock_data

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

@app.get("/stock-data/")
async def get_data(stock: str, days: int, interval: str = "1d"):
    return get_stock_data(stock, days, interval)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
