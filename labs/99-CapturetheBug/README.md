# Capture the Bug – PromQL Challenge

## Story

A major incident affected our e-commerce platform. Several anomalies occurred during a two-hour period.

Your task is to identify every issue using PromQL only.

## Rules

* Use PromQL exclusively.
* Every answer must be supported by a query.
* Assume all metrics are accurate.
* Root-cause hypotheses must be backed by evidence.

## Objectives

Find:

1. Service with the highest error rate.
2. Service causing the payment backlog.
3. Service with abnormal CPU utilization.
4. Service with a memory leak.
5. Service producing excessive database load.
6. Number of failed orders.
7. Deployment involved in the incident.
8. Service with the highest p95 latency.
9. When the latency regression started.
10. Whether the regression correlates with a deployment.

## Hints

* Use `rate()` for counters.
* Use `increase()` to measure impact.
* Use `topk()` to find outliers.
* Use joins with `on()` and `group_left()`.
* Histogram metrics may reveal hidden issues.

Good luck.
