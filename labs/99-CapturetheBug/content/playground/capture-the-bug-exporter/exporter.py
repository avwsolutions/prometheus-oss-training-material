from prometheus_client import start_http_server
from prometheus_client.core import (
    REGISTRY,
    CounterMetricFamily,
    GaugeMetricFamily,
)

import threading
import time


SIMULATION_MINUTES = 120
TICK_SECONDS = 60


LATENCY_BUCKETS = [
    0.1,
    0.25,
    0.5,
    1,
    2.5,
    5,
    10,
]


class IncidentSimulator:

    def __init__(self):

        self.minute = 0

        self.services = [
            "frontend",
            "checkout",
            "payment",
            "inventory",
            "recommendation",
        ]

        #
        # Counters
        #

        self.requests = {
            svc: {
                "200": 0,
                "500": 0,
            }
            for svc in self.services
        }

        self.db_queries = {
            svc: 0
            for svc in self.services
        }

        self.orders_created = 0
        self.orders_completed = 0
        self.orders_failed = 0

        #
        # Gauges
        #

        self.cpu = {
            "frontend": 42,
            "checkout": 48,
            "payment": 34,
            "inventory": 50,
            "recommendation": 30,
        }

        self.memory = {
            svc: int(1.5 * 1024**3)
            for svc in self.services
        }

        self.queue_depth = {
            "orders": 20,
            "inventory": 40,
            "payment": 25,
        }

        #
        # Deployment
        #

        self.payment_version = "3.4.8"

        #
        # Histogram backing storage
        #

        self.histogram_buckets = {
            svc: {
                b: 0
                for b in LATENCY_BUCKETS + ["+Inf"]
            }
            for svc in self.services
        }

        self.histogram_count = {
            svc: 0
            for svc in self.services
        }

        self.histogram_sum = {
            svc: 0.0
            for svc in self.services
        }

    def add_latency_samples(
        self,
        service,
        requests_per_minute,
        degraded=False,
    ):

        if degraded:

            cumulative = {
                0.1: 50,
                0.25: 150,
                0.5: 300,
                1: 450,
                2.5: 700,
                5: 950,
                10: 1000,
                "+Inf": 1000,
            }

            avg_latency = 3.5

        else:

            cumulative = {
                0.1: 700,
                0.25: 950,
                0.5: 995,
                1: 1000,
                2.5: 1000,
                5: 1000,
                10: 1000,
                "+Inf": 1000,
            }

            avg_latency = 0.2

        for bucket, value in cumulative.items():

            self.histogram_buckets[service][bucket] += value

        self.histogram_count[service] += requests_per_minute

        self.histogram_sum[service] += (
            requests_per_minute * avg_latency
        )

    def tick(self):

        if self.minute >= SIMULATION_MINUTES:
            return

        self.minute += 1

        #
        # Incident windows
        #

        payment_error_spike = (
            10 <= self.minute <= 25
        )

        payment_queue_bug = (
            self.minute >= 20
        )

        inventory_cpu_bug = (
            35 <= self.minute <= 50
        )

        deployment_bug = (
            self.minute >= 40
        )

        recommendation_latency_bug = (
            45 <= self.minute <= 65
        )

        frontend_traffic_drop = (
            self.minute >= 55
        )

        #
        # Requests
        #

        for svc in self.services:

            rpm = 1000

            if (
                svc == "frontend"
                and frontend_traffic_drop
            ):
                rpm = 150

            errors = int(rpm * 0.002)

            if (
                svc == "payment"
                and payment_error_spike
            ):
                errors = int(rpm * 0.15)

            self.requests[svc]["200"] += rpm
            self.requests[svc]["500"] += errors

            #
            # DB
            #

            if svc == "payment":
                self.db_queries[svc] += 2500
            else:
                self.db_queries[svc] += 500

            #
            # Histogram
            #

            self.add_latency_samples(
                svc,
                rpm,
                degraded=(
                    svc == "recommendation"
                    and recommendation_latency_bug
                ),
            )

        #
        # Orders
        #

        created = 100

        if payment_error_spike:
            failed = 8
        else:
            failed = 1

        completed = (
            created - failed
        )

        self.orders_created += created
        self.orders_completed += completed
        self.orders_failed += failed

        #
        # Memory leak
        #

        self.memory["checkout"] += (
            15 * 1024 * 1024
        )

        #
        # Queue backlog
        #

        if payment_queue_bug:

            self.queue_depth["payment"] = min(
                2500,
                self.queue_depth["payment"] + 80
            )

        #
        # CPU issue
        #

        if inventory_cpu_bug:
            self.cpu["inventory"] = 98
        else:
            self.cpu["inventory"] = 50

        #
        # Deployment
        #

        if deployment_bug:
            self.payment_version = "3.4.9"


SIM = IncidentSimulator()


def simulation_thread():

    while SIM.minute < SIMULATION_MINUTES:

        SIM.tick()

        print(
            f"Simulation minute "
            f"{SIM.minute}/{SIMULATION_MINUTES}"
        )

        time.sleep(TICK_SECONDS)

    print(
        "Simulation complete. "
        "Timeline frozen."
    )

    while True:
        time.sleep(3600)


class IncidentCollector:

    def collect(self):

        #
        # Status
        #

        sim = GaugeMetricFamily(
            "simulation_minute",
            "Current simulation minute",
        )

        sim.add_metric(
            [],
            SIM.minute,
        )

        yield sim

        status = GaugeMetricFamily(
            "challenge_completed",
            "Timeline completed",
        )

        status.add_metric(
            [],
            1 if SIM.minute >= 120 else 0,
        )

        yield status

        #
        # Requests
        #

        requests = CounterMetricFamily(
            "http_requests_total",
            "Requests",
            labels=["service", "status"],
        )

        for svc in SIM.services:

            requests.add_metric(
                [svc, "200"],
                SIM.requests[svc]["200"],
            )

            requests.add_metric(
                [svc, "500"],
                SIM.requests[svc]["500"],
            )

        yield requests

        #
        # CPU
        #

        cpu = GaugeMetricFamily(
            "service_cpu_usage_percent",
            "CPU",
            labels=["service"],
        )

        for svc, value in SIM.cpu.items():

            cpu.add_metric(
                [svc],
                value,
            )

        yield cpu

        #
        # Memory
        #

        memory = GaugeMetricFamily(
            "service_memory_usage_bytes",
            "Memory",
            labels=["service"],
        )

        for svc, value in SIM.memory.items():

            memory.add_metric(
                [svc],
                value,
            )

        yield memory

        #
        # Queue
        #

        queue = GaugeMetricFamily(
            "queue_depth",
            "Queue depth",
            labels=["queue"],
        )

        for q, value in SIM.queue_depth.items():

            queue.add_metric(
                [q],
                value,
            )

        yield queue

        #
        # DB
        #

        db = CounterMetricFamily(
            "db_queries_total",
            "DB Queries",
            labels=["service"],
        )

        for svc, value in SIM.db_queries.items():

            db.add_metric(
                [svc],
                value,
            )

        yield db

        #
        # Orders
        #

        created = CounterMetricFamily(
            "orders_created_total",
            "Orders created",
        )

        created.add_metric(
            [],
            SIM.orders_created,
        )

        yield created

        completed = CounterMetricFamily(
            "orders_completed_total",
            "Orders completed",
        )

        completed.add_metric(
            [],
            SIM.orders_completed,
        )

        yield completed

        failed = CounterMetricFamily(
            "orders_failed_total",
            "Orders failed",
        )

        failed.add_metric(
            [],
            SIM.orders_failed,
        )

        yield failed

        #
        # Deployment
        #

        deployment = GaugeMetricFamily(
            "deployment_info",
            "Deployment",
            labels=["service", "version"],
        )

        deployment.add_metric(
            ["frontend", "1.9.2"],
            1,
        )

        deployment.add_metric(
            ["checkout", "2.1.0"],
            1,
        )

        deployment.add_metric(
            ["inventory", "2.0.1"],
            1,
        )

        deployment.add_metric(
            ["recommendation", "1.4.1"],
            1,
        )

        deployment.add_metric(
            ["payment", SIM.payment_version],
            1,
        )

        yield deployment

        #
        # Histogram buckets
        #

        buckets = CounterMetricFamily(
            "http_request_duration_seconds_bucket",
            "Latency buckets",
            labels=["service", "le"],
        )

        for svc in SIM.services:

            for bucket, value in (
                SIM.histogram_buckets[svc].items()
            ):

                buckets.add_metric(
                    [svc, str(bucket)],
                    value,
                )

        yield buckets

        count = CounterMetricFamily(
            "http_request_duration_seconds_count",
            "Latency count",
            labels=["service"],
        )

        for svc, value in (
            SIM.histogram_count.items()
        ):

            count.add_metric(
                [svc],
                value,
            )

        yield count

        latency_sum = CounterMetricFamily(
            "http_request_duration_seconds_sum",
            "Latency sum",
            labels=["service"],
        )

        for svc, value in (
            SIM.histogram_sum.items()
        ):

            latency_sum.add_metric(
                [svc],
                value,
            )

        yield latency_sum


REGISTRY.register(
    IncidentCollector()
)

threading.Thread(
    target=simulation_thread,
    daemon=True,
).start()

start_http_server(8000)

print(
    "Capture-the-bug exporter "
    "listening on :8000"
)

while True:
    time.sleep(3600)