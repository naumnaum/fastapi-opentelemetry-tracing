import os
from fastapi import FastAPI
from asyncio import sleep as async_sleep
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
APP_1_PORT = int(os.getenv("APP_1_PORT"))


class MessageResponse(BaseModel):
    message: str


@app.get("/query/{seconds}", response_model=MessageResponse)
async def query(seconds: int):
    await async_sleep(seconds)
    response = MessageResponse(
        message=f"APP2: Asynchronous delay for {seconds} seconds"
    )
    return response
