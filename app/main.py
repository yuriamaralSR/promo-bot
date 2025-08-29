from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    debug_mode = os.getenv("DEBUG")
    return {"message": f"PromoBot API - Debug: {debug_mode}"}