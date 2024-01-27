import os
from fastapi import FastAPI, Request
from time import sleep
from dotenv import load_dotenv
from pydantic import BaseModel
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from otel.common import configure_tracer
from loguru import logger

tracer = configure_tracer(name="app_2", version="1.0.0")
load_dotenv()
app = FastAPI()
APP_1_PORT = int(os.getenv("APP_1_PORT"))


class Response(BaseModel):
    message: str


def get_delay_message() -> str:
    with tracer.start_as_current_span("get_delay_message"):
        seconds = 2
        sleep(seconds)
        message = f"APP2: Asynchronous delay for {seconds} seconds"
        return message


@app.get("/delay", response_model=Response)
async def delay(request: Request):
    traceparent = request.headers.get("traceparent")
    logger.info(f"traceparent: {traceparent}")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("GET /delay", context=trace_context):
        delay_message = get_delay_message()
        return Response(message=delay_message)
