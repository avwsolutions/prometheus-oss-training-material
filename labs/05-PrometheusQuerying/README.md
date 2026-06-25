# Introduction lab exercises

Welcome to the Prometheus Querying lab exercises. During the lab exercises the student will experiential work through various tasks and activities to gain practical experience and develop new skills. In hands-on learning, attendees are given the opportunity to explore, experiment, and discover knowledge for themselves about the legendary Elastic Stack.

The goal is to get actively engage and ask questions if something is not clear or you are blocked. Important to understand that there are no strong dependencies between labs, so it's okay if you're behind and follow your own pace.

The following key topics are part of these exercises:

- Playing Prometheus Bingo game
- Comparing Client library against OpenTelemetry
- Hands-on with Beginner PromQL queries
- Challenge yourself with Intermediate PromQL queries

## Exercise 1 - Playing Prometheus Bingo game

This first exercise you are going to learn more about the `Pushgateway` and implement a `Push-based` job called `prometheus_bingo_drew_generator`.  

What does this job exactly do:

- Pushes a `Counter`.
- Metric provides both the *number* and **bingo** if it's celebration time!

> [!NOTE]  
> Since you already are familiar with most concepts like the *container* setup and *jobs*, not every step is fully explained.

### Exercise 1.1 - Configure the pushGateway

The following tasks need to be completed, before you can run the actually job.

Complete the following tasks to update your *prometheus-playground*:

- Ensure that the *pushgateway* service is available in the `compose.yml`.
- Ensure that a valid *scraping job* is created for the *pushgateway*. Take the other (like *node-exporter*) as example and ensure port *9091* is scraped.
- Validate using the `Prometheus UI` is the target is online and available.

### Exercise 1.2 - Start the Bingo game job

Great. Now let's generate some metrics. Again it's all about fun, so we just play *random* bingo. the code can be found here [bingo-game](./content/bingo-game/bingo.py).

Only activity here is to start the actual job. You may want to execute [run.sh](./content/bingo-game/run.sh). or follow the steps below. Ensure you are in the *bingo-game* folder.

```
python -m venv lab05
source lab05/bin/activate # lab05\Scripts\activate
pip install prometheus-client
./bingo.py
```

### Exercise 1.3 - Start playing Bingo

Since you have the job running you might already have completed some Bingo rounds. Great, lets dive into the data and ask the following questions using `PromQL`.

Now answer the following questions:

- What are the top 10 numbers?
- What are the top 10 lucky numbers?
- Which numbers are drawn in the last 5 minutes?
- Can you calculate the Win-ratio?  So wins compared against bingo rounds.

Write down all queries and discuss them with the other students.

## Exercise 2 - Comparing Client library against OpenTelemetry

This exercise you will learn about the key differences implementing the Prometheus *client library* and a *OpenTelemetry* based alternative. You start by implementing the *Sales App* intrumentation using the native rometheus *client library* and analyze those metrics. Second task is implementing the *OpenTelemetry* based *Sales App* instrumentation, including all necessary prerequisites.

Let's get started!

### Exercise 2.1 - Integrate Sales App metrics

Here we take the quick route by including the *build* context for the *sales-app* into `compose.yml`. The example below expects the *sales-app* folder in the same folder as the `compose.yml`.

The following tasks need to be completed, before you can run the actually new service.

Complete the following tasks to update your *prometheus-playground*:

- Copy the [sales-app](./content/sales-app/) to your *prometheus-playground* (root) folder.
- Update the `compose.yml` with a new *service* called `sales-app`.

```
sales-app:
    build:
      context: sales-app
    container_name: sales-app
    restart: ${RESTART_POLICY}
    ports:
      - 8000:8000
```
- Ensure you also add a scraping job to the `prometheus.yml` configuration and set the *label* to *app: "sales"*.

### Exercise 2.2 - Explore the client library created metrics

Here you are going to inspect the metrics. During this you are going to ask and write down the following questions:

- Which metrics are exposed?
- Can you generate traffic for both metrics?
- How many requests did the service already handled?
- What is the average amount of sessions the last 5 minutes? Can you manipulate this?

### Exercise 2.3 - Integrate Sales App metrics using Otel

Now that you have experimented with `client library` based instrumentation, let's spin-up almost the same setup using `OpenTelemetry`.

First we need to connect a `otel-collector`, which is the component that actually collects the telemetry.

- Update the `compose.yml`. Example snippet below.

```
  otel-collector:
    image: otel/opentelemetry-collector-contrib:${OTEL_COLLECTOR_VERSION}
    container_name: otel-collector
    restart: ${RESTART_POLICY}
    command:
      - "--config=/etc/otelcol-contrib/config.yml"
    volumes:
      - ./config/otel-collector/config.yml:/etc/otelcol-contrib/config.yml:ro
    ports:
      - "${OTEL_GRPC_PORT}:4317"
      - "${OTEL_HTTP_PORT}:4318"
      - "${OTEL_METRICS_PORT}:8888"
      - "${OTEL_PROMETHEUS_EXPORT_PORT}:8889"
```
- Ensure you have the [config.yml](./content/otel-sales-app/config.yml) available under the config structure.
- You may already see two ports [8888, 8889] which we can create a scape job for.
- After setting all configuration, update/restart the containers and if needed restart prometheus container. The service must be visible as container called `otel-collector`.
- Validate using the `Prometheus UI` if both targets are online and available.

### Exercise 2.4 - Deploy and analyse Otel metrics against Prometheus metrics

This last exercise you are going to deploy the actual updated code. You can see the changes here [app.py](./content/otel-sales-app/app.py). In essence, it's just another container image, but it's not as straightforward you expect.

Below the steps to activate the container to analyze the metrics.

- Copy over the [otel-sales-app](./content/otel-sales-app/) to your Prometheus playground.
- Just like the previous example, you have to add the *service* called `0tel-sales-app` to the `compose.yml`, including a *build context*. You may want to see how you did this during exercise 2.1. 
- Also to prevent port collaps we use port `8080` instead of `8000`.
- Include [environment variables](./content/otel-sales-app/.env-example) to the service under *environment:*.
- Since it depends upon the `otel-collector`, you may want add it as a `dependency`.
- If everything is added you can update/restart all containers.

If everything works (including connectivity) you should see metrics. For troubleshooting I advise to have a look into the container logs:

- Inspect otel-sales-app logs (`docker logs otel-sales-app` ).
- Inspect otel-collector logs.
- Repeat the following exercises.
  - Which metrics are exposed?
  - Can you generate traffic for both metrics?
  - How many requests did the service already handled?
  - What is the average amount of sessions the last 5 minutes? Can you manipulate this?

- Write down the pros & cons you discover of using *Otel vs Native integration*. Think about delays, complexity, etc.

### Bonus exercise 2.5 - Connect the Otel Collector directly using the OTLP Receiver

As you may have noticed we have used the *scraping* approach. With recent *Prometheus deployments* you can also leverage the `OTLP Receiver`.

- Reconfigure Prometheus to expose the `OTLP Receiver endpoint`.
- Ensure that the *recommended parameters* are configured in the *prometheus.yml*.
- Reconfigure the Otel receiver configuration in the *config.yml*.

## Exercise 3 - Hands-on with Beginner PromQL queries

These first hands-on exercises you are going to learn the basics of using the `PromQL` syntax and Operators. You already should be a little bit familiar with them. For the queries below you will use the `Node Exporter` delivered metrics.

### Exercise 3.1 - Simple metric queries

This exercise you will look at `node_memory_MemTotal_bytes`.

- Return all metrics for node_memory_MemTotal_bytes.
- Can you filter them by instance?
- Can you use Regex to filter to only certain (one or more) label values?

Create and execute those queries, you think that are required.

### Exercise 3.2 - Using basic operator

This exercise you will look at both `node_memory_MemTotal_bytes` and `node_memory_MemAvailable_bytes`. Using basic operators we can easily calculate percentages. In this example.

- Start with a *division* to calculate memory used as *fraction of total*.
- Now try to convert this *fraction of total* to a percentage.

Create and execute those queries. First query is 70% of the second query.

### Exercise 3.3 - Time ranges and basic functions

This exercise you will look at `node_cpu_seconds_total` metric. We first pick a time range and play around with basic functions like *count*, *avg*, *sum*, etc.

- Get the sum of all CPU time for idle mode.
- Get the avg of all CPU time for system mode.
- Get the count of all CPU's available.
- What is needed when multiple instances are available?

## Bonus exercise 4 - Challenge yourself with Intermediate PromQL queries

These bonus hands-on exercises you are going to dig a little bit deeper using the `PromQL` syntax and Operators. You already got familiar with the basics. For the queries below you will use the `Node Exporter` delivered metrics.

### Exercise 4.1 - Calculate using rate() and increase() function

This exercise you are going to apply both rate() and increase() functions. In the beginning both seem to be equal, but looking into the details they behave differently. You will learn about the differences solving the questions below.

- Can you calculate the CPU *per-second Usage* per mode?
- how can you make ensure that it only shows the Top 5 modes?
- Can you calculate a *total seconds used*  per mode?
- Explain when and why you either used rate() or increase()

### Exercise 4.2 - Memory usage calculation

This excercise you are going to look back into a previous metric query to calculate the percentage of memory usage. This thing is that you can do this in several ways. Sometimes this can make you confused (and some colleagues during a discussion). 

You may have used the following  query:

```
100 * ((node_memory_MemTotal_bytes{instance="node-exporter:9100"} - node_memory_MemAvailable_bytes{instance="node-exporter:9100"}) / node_memory_MemTotal_bytes{instance="node-exporter:9100"})
```
> Hint:
>  You following query style is used `(1 - (node_memory_MemAvailable_bytes .....`

- Which metric query will give you the same result?


The following question you are going to use both `node_filesystem_free_bytes` and `node_filesystem_size_bytes` metric.

- Now reuse this query style to calculate the disk usage, in percentage,  for the '/' mount.


### Exercise 4.3 - Network and load calculations

This excercise you are going to reuse some practices and learn how to do load comparisons.

- Create a two metric queries that shows the network receive and transmit rate per instance of the last 5 minutes.
- What's the overall receive/transmit ratio for the host?

> Hint: sum by instance rate receive/sum by instance rate transmit.

-  The query below doesn't show any output. Explain what the output tells you. 

```
node_load1 > count(node_cpu_seconds_total{mode="idle"})
```

## Next Steps

You are ready to start with the Sixth lab about [Prometheus Alerting](../06-PrometheusAlerting/README.md) for Prometheus Alertmanager. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
