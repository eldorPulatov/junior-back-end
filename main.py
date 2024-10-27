from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from client import Database
import uvicorn

app = FastAPI()
database = Database()

@app.on_event("startup")d
async def startup_event():
    await database.init_db()

@app.get("/prices/all")
async def get_all_prices(ticker: str = Query(...)):
    data = await database.get_all_prices(ticker)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/prices/latest")
async def get_latest_price(ticker: str = Query(...)):
    data = await database.get_latest_price(ticker)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/prices/by_date")
async def get_prices_by_date(ticker: str = Query(...), date: int = Query(...)):
    data = await database.get_prices_by_date(ticker, date)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
