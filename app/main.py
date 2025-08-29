from fastapi import FastAPI
from app.core.scraper.shopee_api import ShopeeAPIClient

app = FastAPI()
shopee_client = ShopeeAPIClient()

@app.get("/")
async def root():
    return {"message": "Welcome to the Shopee Offers API"}

@app.get("/offers")
async def get_offers():
    offers = shopee_client.fetch_offers()
    return {"offers": offers[:5]}