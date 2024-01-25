from fastapi import FastAPI, HTTPException, BackgroundTasks
from random import randint, choice
import httpx
from time import sleep
from asyncio import sleep as async_sleep

app = FastAPI()

# JSONPlaceholder URL for demonstration
json_placeholder_url = "https://jsonplaceholder.typicode.com/posts"


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app."}


@app.get("/sync-delay/{seconds}")
def sync_delay(seconds: int):
    """Synchronous delay."""
    sleep(seconds)
    return {"message": f"Synchronous delay for {seconds} seconds"}


@app.get("/async-delay/{seconds}")
async def async_delay(seconds: int):
    """Asynchronous delay."""
    await async_sleep(seconds)
    return {"message": f"Asynchronous delay for {seconds} seconds"}


@app.get("/random-error")
def random_error():
    """Randomly raises an error."""
    if randint(0, 1):
        raise HTTPException(status_code=500, detail="Random Internal Server Error")
    return {"message": "No error this time"}


@app.get("/call-external")
async def call_external():
    """Calls an external service."""
    async with httpx.AsyncClient() as client:
        response = await client.get(json_placeholder_url)
        response.raise_for_status()
    return {"external_service_url": json_placeholder_url, "response": response.json()}


@app.get("/background-task")
def background_task(background_tasks: BackgroundTasks):
    """Executes a background task."""
    background_tasks.add_task(some_background_task)
    return {"message": "Background task initiated"}


def some_background_task():
    """A dummy background task."""
    sleep(5)
    print("Background task completed")


@app.get("/chain-requests")
async def chain_requests():
    """Chains multiple internal requests."""
    async with httpx.AsyncClient() as client:
        delay_response = await client.get("http://0.0.0.0:80/sync-delay/1")
        echo_response = await client.get("http://0.0.0.0:80/echo/Chained call")
        error_response = await client.get("http://0.0.0.0:80/random-error")

    return {
        "delay_response": delay_response.json(),
        "echo_response": echo_response.json(),
        "error_response": error_response.json(),
    }
