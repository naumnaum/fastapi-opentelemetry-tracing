import os
from fastapi import FastAPI
import httpx
import aiohttp
from asyncio import sleep as async_sleep
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
app = FastAPI()

# JSONPlaceholder URL for demonstration
json_placeholder_url = "https://jsonplaceholder.typicode.com/posts"
APP_1_PORT = int(os.getenv("APP_1_PORT"))
APP_2_PORT = int(os.getenv("APP_2_PORT"))

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app."}


@app.get("/async-delay/{seconds}")
async def async_delay(seconds: int):
    """Asynchronous delay."""
    await async_sleep(seconds)
    return {"message": f"APP_1: Asynchronous delay for {seconds} seconds"}


@app.get("/call-external")
async def call_external():
    """Calls an external service."""
    async with httpx.AsyncClient() as client:
        response = await client.get(json_placeholder_url)
        response.raise_for_status()
    return {"external_service_url": json_placeholder_url, "response": response.json()}


@app.get("/multiservice-wait/")
async def chain_requests(seconds: int | None = 2):
    """Chains multiple internal requests."""
    session = aiohttp.ClientSession()
    async with session.get(f"http://app_1:{APP_1_PORT}/async-delay/{seconds}") as response:
        response_internal = await response.json()
    async with session.get(f"http://app_2:{APP_2_PORT}/query/{seconds}") as response:
        response_external = await response.json()
    combined_response = {
        "response_internal": response_internal,
        "response_external": response_external
    }
    await session.close()
    return combined_response
