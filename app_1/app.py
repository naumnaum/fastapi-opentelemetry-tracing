import os
from typing import Dict

from fastapi import FastAPI, Request
import httpx
import aiohttp
from time import sleep
from dotenv import load_dotenv
from loguru import logger
import secrets
from pydantic import BaseModel
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from otel.common import configure_tracer

tracer = configure_tracer(name="app_1", version="1.0.0")

load_dotenv()
app = FastAPI()

# JSONPlaceholder URL for demonstration
json_placeholder_url = "https://jsonplaceholder.typicode.com/posts"
APP_1_PORT = int(os.getenv("APP_1_PORT"))
APP_2_PORT = int(os.getenv("APP_2_PORT"))


class Response(BaseModel):
    message: str


def debugging():
    sleep(2)


async def get_message_app_2():
    # Starting a trace
    with tracer.start_as_current_span("get_message_app_2"):
        debugging()  # Injecting sleep() to illustrate the work of tracing
        # Generating header to propagate to app_2
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        headers = carrier
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://app_2:{APP_2_PORT}/delay",
                headers=headers,
            ) as response:
                response = await response.json()
        return response


# A dummy function to imitate the header from initial request
def get_initial_header() -> Dict[str, str]:
    version = "00"
    trace_id = secrets.token_hex(16)
    span_id = secrets.token_hex(8)
    trace_flags = "01"
    headers = {"traceparent": f"{version}-{trace_id}-{span_id}-{trace_flags}"}
    return headers


@app.get("/multiservice-request", response_model=Response)
async def chain_requests(request: Request):
    # Extracting info from request about the parent trace
    traceparent: str = get_initial_header().get("traceparent")
    logger.info(f"traceparent: {traceparent}")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span(
        "GET /multiservice-request", context=trace_context
    ):
        response_from_app_2 = await get_message_app_2()
        response = Response(message=response_from_app_2["message"])
        return response


# TODO: Implement tracing using external APIs
@app.get("/call-external")
async def call_external():
    """Calls an external service."""
    async with httpx.AsyncClient() as client:
        response = await client.get(json_placeholder_url)
        response.raise_for_status()
    return {"external_service_url": json_placeholder_url, "response": response.json()}
