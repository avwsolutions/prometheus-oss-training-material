#!/usr/bin/env python3

import random
import time
from collections import defaultdict

from prometheus_client import CollectorRegistry, Counter, push_to_gateway

PUSHGATEWAY = "http://localhost:9091"
JOB_NAME = "prometheus_bingo_drew_generator"

# Keep counters in memory
draw_counts = defaultdict(int)

while True:
    number = random.randint(1, 75)
    bingo = random.choice(["yes", "no"])

    draw_counts[(str(number), bingo)] += 1

    registry = CollectorRegistry()

    metric = Counter(
        "prometheus_bingo_draw_total",
        "Total number of bingo draws",
        ["number", "bingo"],
        registry=registry,
    )

    # Rebuild counters from accumulated state
    for (num, bingo_label), count in draw_counts.items():
        metric.labels(number=num, bingo=bingo_label)._value.set(count)

    push_to_gateway(
        PUSHGATEWAY,
        job=JOB_NAME,
        registry=registry,
    )

    print(
        f"Pushed number={number}, bingo={bingo}, "
        f"count={draw_counts[(str(number), bingo)]}"
    )

    time.sleep(10)