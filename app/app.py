from fastapi import FastAPI
from time import sleep
import logging
import numpy

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/delay/{seconds}")
async def delay_response(seconds: int):
    sleep(seconds)
    return {"message": f"Delayed for {seconds} seconds"}


@app.get("/echo/{message}")
async def echo_message(message: str):
    return {"echo": message}
