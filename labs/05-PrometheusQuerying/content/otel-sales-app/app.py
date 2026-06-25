from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from opentelemetry import metrics
import asyncio

app = FastAPI()

# Uses the MeterProvider configured by OpenTelemetry auto-instrumentation
meter = metrics.get_meter("sales-app")

# Custom metric for concurrent in-flight requests
requests_in_progress = meter.create_up_down_counter(
    name="otel_active_sessions_count",
    description="Number of currently active HTTP requests",
    unit="1",
)


@app.middleware("http")
async def track_inflight_requests(request: Request, call_next):
    requests_in_progress.add(
        1,
        {
            "http.route": request.url.path,
        },
    )

    try:
        response = await call_next(request)
        return response

    finally:
        requests_in_progress.add(
            -1,
            {
                "http.route": request.url.path,
            },
        )


@app.get("/", response_class=PlainTextResponse)
async def root():
    await asyncio.sleep(15)
    return "Under Observation"