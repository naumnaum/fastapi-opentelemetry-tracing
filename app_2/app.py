import os
from fastapi import FastAPI
from asyncio import sleep as async_sleep
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
APP_1_PORT = int(os.getenv("APP_2_PORT"))

@app.get("/query/{seconds}")
async def query(seconds: int):
    await async_sleep(seconds)
    return {"message": f"APP2: Asynchronous delay for {seconds} seconds"}
