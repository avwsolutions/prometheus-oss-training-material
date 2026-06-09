# Introduction lab exercises

Welcome to the Observability Primer lab exercises. Throughout these exercises, participants will engage in a series of practical tasks and activities designed to build hands-on experience and develop key observability skills. Attendees will have the opportunity to explore, experiment, and deepen their understanding of modern observability concepts and practices, with a particular focus on Prometheus.

The goal of these lab exercises is to actively engage with the material and ask questions whenever something is unclear or you encounter a blocker. It is important to note that there are no strict dependencies between the labs, so it is perfectly fine to progress at your own pace, even if you fall behind on a particular exercise.

The following key topics are covered throughout these exercises:

* Downloading training resources
* Selecting an appropriate diagnostic model
* Defining a Service Level Objective (SLO)

## Exercise 1 - Downloading training resources

This first exercise you are required to download the training resources. You only need to download one package.

Most simply way is using Curl or [Download the ZIP](https://github.com/avwsolutions/prometheus-oss-training-material/archive/refs/heads/main.zip) using your favorite browser. Git is not part of this course, but we encourage using the Git client, which you can [download](https://git-scm.com/downloads/guis) for free.

Either choose one of the options to download the training material.

### Exercise 1.1 - Download using Curl

First the lab material and second the Second the deployment code.

```
cd
curl -L https://github.com/avwsolutions/prometheus-oss-training-material/archive/refs/heads/main.zip -o prometheus-oss-training-material.zip
unzip prometheus-oss-training-material-main.zip
mv prometheus-oss-training-material-main prometheus-oss-training-material
```

### Exercise 1.2 - Download using Git

```
cd
git clone https://github.com/avwsolutions/prometheus-oss-training-material.git
```

If you want to know more about Git, the Version Control System just visit the [Git-SCM Website](https://git-scm.com/).

Now that you have downloaded the material (and extracted the ZIP file) you may want to look into this directory.

```
cd ~/prometheus-oss-training-material
ls
```

# Casus lab exercises

## Casus - Containerized Web Application

A company hired you to setup a *greenfield* Observability platform for their new e-commerce platform called **ShopNow**. The platform runs on a Kubernetes cluster and consists of several microservices/compoents:

- Frontend web application
- Product catalog API
- Shopping cart service
- Payment service
- PostgreSQL database
- Redis cache
- Ingress controller for external traffic

The platform serves *approximately 50,000 users per day*. During promotions, traffic can increase five times

### Business requirements

- Customers must be able to browse products and complete purchases with minimal delays.
- Failed payments directly impact revenue.
- Customer complaints increase significantly if checkout takes more than 3 seconds.
- Planned maintenance occurs *monthly* during a short maintenance window.
- The company estimates that *less than 45 minutes of unexpected downtime per month is acceptable*.

## Exercise 1 - Select a Diagnostic Model (RED, USE, or Golden Signals)

Since you are responsible for the new *greenfield* Observability platform you have to decide which diagnostic model to choose for implementing the applicable metrics.

Choose one of the following diagnostic models:

- RED Method
- USE Method
- Golden Signals

You may want to conduct [Grafana - Observability strategies](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/).

Now answer the following questions:
- Explain why your selected model is the best fit for this casus.
- Describe which metrics you would measure.
- Explain how you would measure them in a Kubernetes/container environment.
- Identify at least three components where these measurements should be implemented.

### Exercise 2 -Define an SLO based on requirements

This next exercise you are goingi to dive into defining a draft *Service Level Objective* based on the **ShopNow** business requirements. Read the casus and requirements carefully and write down the desired SLO.

Hint:
- SLO is set in percentage.
- SLI you can formulate a sentence like *.... requests respond within 3 seconds*
- Measurement method you can just pick the SLI type.

You may want to conduct [Grafana - SLO Implementation](https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/).

Now answer the following questions:
- Select a service for which an SLO is important (for example checkout, payments, or product browsing).
- Define the SLI (Service Level Indicator), SLO (Service Level Objective) and measurement method.
- Explain why you think this SLO supports the business requirements.
- Describe what happens if the error budget is consumed.

## Next Steps

You are ready to start with the second lab about [Prometheus Introduction](../02-PrometheusIntroduction/README.md) for Prometheus. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
