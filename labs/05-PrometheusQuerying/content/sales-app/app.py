from fastapi import FastAPI, Request
from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from fastapi.responses import PlainTextResponse, Response
import asyncio

app = FastAPI()

# Total requests to "/"
REQUEST_COUNTER = Counter(
    "sales_web_requests_total",
    "Total number of requests to the Sales endpoint."
)

# Concurrent open requests
OPEN_SESSIONS = Gauge(
    "sales_active_sessions_count",
    "Number of currently active requests to the Sales App."
)


@app.middleware("http")
async def track_sessions(request: Request, call_next):
    OPEN_SESSIONS.inc()

    try:
        response = await call_next(request)
        return response
    finally:
        OPEN_SESSIONS.dec()


@app.get("/", response_class=PlainTextResponse)
async def root():
    REQUEST_COUNTER.inc()
    await asyncio.sleep(15)

    return "Under Observation"


@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )