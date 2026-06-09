# Introduction lab exercises

Welcome to the Observability Primer lab exercises. Throughout these exercises, participants will engage in a series of practical tasks and activities designed to build hands-on experience and develop key observability skills. Attendees will have the opportunity to explore, experiment, and deepen their understanding of modern observability concepts and practices, with a particular focus on Prometheus.

The goal of these lab exercises is to actively engage with the material and ask questions whenever something is unclear or you encounter a blocker. It is important to note that there are no strict dependencies between the labs, so it is perfectly fine to progress at your own pace, even if you fall behind on a particular exercise.

The following key topics are covered throughout these exercises:

- Download Prometheus
- Getting started with Prometheus

## Exercise 1 - Download Prometheus

This exercise you are going to download the `Prometheus` package. This package is required for the following exercises.

It's your decision, but you can either chose `LTM` or `latest` release. Which do you prefer for Production?

The labs are build and testing using release version **3.11.3 / 2026-04-27**.

Open the page [Prometheus Download page](https://prometheus.io/download/) and download the Linux packages for *prometheus*, *alertmanager*, *blackbox_exporter*, *node_exporter* and *pushgateway*. Store them on your Linux host (e.g. Home downloads) for later usage.

For CLI users you may want to use Curl.

```
curl -L https://github.com/prometheus/prometheus/releases/download/v3.12.0/prometheus-3.11.3.linux-amd64.tar.gz -O
curl -L https://github.com/prometheus/alertmanager/releases/download/v0.32.2/alertmanager-0.32.2.darwin-amd64.tar.gz -O
curl -L https://github.com/prometheus/blackbox_exporter/releases/download/v0.28.0/blackbox_exporter-0.28.0.darwin-amd64.tar.gz -O
curl -L https://github.com/prometheus/node_exporter/releases/download/v1.11.1/node_exporter-1.11.1.darwin-amd64.tar.gz -O
curl -L https://github.com/prometheus/pushgateway/releases/download/v1.11.3/pushgateway-1.11.3.darwin-amd64.tar.gz -O
```

## Exercise 2 - Getting Started with Prometheus

This exercise you will get started with Prometheus. Here you will start with the basics by initiating your own `Prometheus Server`.

If your `Prometheus Server` is *up and running* you will explore the provided endpoints and learn more about the `Expression Browser`.

Take a moment to explore the `Prometheus UI` and try to discover all components. You may find out the deployed `version`.

### Exercise 2.1 - Start your first Prometheus Server

Now that you have all packages we can start jumping into *Prometheus*. If you are familiar with Linux starting Prometheus doesn't take much time!

First we are going to copy over *tar.gz* and inspect the *package*.

```
mkdir ~/prometheus
cd ~/prometheus
tar tvfz prometheus-*.tar.gz
```

Now inspect the provided `prometheus.yml`. Don't forget to change folder using `cd prometheus*linux-amd64`.

```
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
       # The label name is added as a label `label_name=<label_value>` to any timeseries scraped from this config.
        labels:
          app: "prometheus"
```

You can use the provided tool called `promtool` to validate the YAML configuration file.

```
./promtool check config prometheus.yml
Checking prometheus.yml
 SUCCESS: prometheus.yml is valid prometheus config file syntax
```

If all looks good, let's inspect the flags you could provide and start the `Prometheus Server` with minimal settings.

```
./prometheus --help
./prometheus --config.file=prometheus.yml # Use & if you want to run it as background job
```

You can also check if your `Prometheus Server` is ready and open for Business.
```
./promtool check ready
  SUCCESS:  Prometheus Server is Ready.
```

### Exercise 2.2 - Explore the Expression Browser

Open the `URL` with a modern browser like Chrome, Edge or Firefox. Ensure that you include the `Prometheus Port`, which is `9090`. No login credentials are required.

When the page is loaded successfully you will see the following page appear, which is the `Expression Browser`.

[Expression Browser](./content/prometheus-expression-browser.png)

The `Expression Browser` is a console which makes it possible to enter query expressions you can execute. To make things easier you can open the `Query Options` by clicking on the *three dots*  on the right and pick *Explore Metrics*.

Now answer the following questions:
- For which components are currently metrics available? how did you recognize them?
- Can you filter *prometheus* only metrics?
- Lookup how much *Go Threads* are started and write down the result.
- Which option must be enabled to use the *Explain view*?
- If the option is enabled, discuss and explain with a fellow student which *Metric* you used to figure out the running *Go Threads*.

### Exercise 2.3 - Understanding Server Status information

Besides the *Query Endpoint* you can also explore to other pages that show `Status Information` and the actual `Prometheus Configuration` for your `Prometheus Server`.

You will find them under *Status* menu item. See the example screen below.

[Server Status](./content/prometheus-status-config.png)

This information is provided by two other endpoints:

| Endpoint |  Description |
| ---------|--------------|
| '/query'  | Expression Browser to execute queries against Prometheus metrics. |
| '/status' | Prometheus Server build and runtime information. |
| '/config' | Prometheus Server loaded configuration. |

> [!NOTE]  
> Currently, neither the "Monitoring Status" and other "Server Status" items are covered. However, these will not be forgotten and will be addressed in one of the following modules.

Now answer the following question:
- What is the current Prometheus version you are running?

As you may already learned, Prometheus is written in *Golang* and like most *Container* optimzed workloads build using *Go*.

Now answer the following question:
- Which Go version is used to build your Prometheus release?
- Compare the results with your fellow students. Did they chose the same release?

The `Prometheus Configuration` file helps to set certain important settings. Some setttings have impact on the *Server status*, such as *Storage Retention*.

Another important thing to monitor are *WAL Corruptions*. Luckily *Prometheus Server* can repair most of them during startup, but large amount can indicate storage issues.

Now answer the following questions:
- What is the default *Storage Retention* set by Prometheus?
- Do you have any *WAL Corruptions*?

Before you are going through the last questions, let's explain the `Prometheus Configuration` page. As you already seen it's formatted as **YAML** and contains several *Configuration sections*. *Global* section helps to *provide defaults*, such as intervals, limits, labels or timeouts for all underlying sections like *runtime*, *storage* and others that extend functionality like *alerting*, *scrape_configs* and *oltp*.

It's important to understand that it provides the *full configuration*, rather then the *provided configuration*.

Now answer the following questions:
- Compare the *Configuration page* and the actual `prometheus.yml`? Which sections are added dynamically?
- What is the default scrape interval and timemout?
- Explain what is configured using *gogc* and why is important.

As you may recognize, all *prometheus* metrics are scraped using the *prometheus* scraping job. Through the page you see all applicable settings, also the *defaults* are inherited. You can also catch real-time updates to the configuration. Let's give this a try.

Now answer the following questions:
- Which path (endpoint) is used to gather the metrics?

Now do the following tasks:
- Edit the `prometheus.yml` and add configure the *retention time* to 7d.

```
storage:
  tsdb:
    out_of_order_time_window: 30d
    retention:
      time: 7d
```
- Now reload your `Prometheus Server` by a restart or use `pkill`.

```
pkill -SIGHUP prometheus

time=2026-05-26T09:54:58.579Z level=INFO source=main.go:1632 msg="Loading configuration file" filename=prometheus.yml
time=2026-05-26T09:54:58.596Z level=INFO source=main.go:1671 msg="Completed loading of configuration file" db_storage=713.323µs remote_storage=2.97µs web_handler=1.828µs query_engine=2.078µs scrape=15.544995ms scrape_sd=12.73µs notify=197.792µs notify_sd=4.229µs rules=2.426µs tracing=2.667µs filename=prometheus.yml totalDuration=16.974798ms
```

- Now refresh the configuration page and verify that your changes have been applied.
- You may see two *outofordertimewindow* settings being applied. Explain what is the difference.


## Next Steps

You are ready to start with the next lab about [Prometheus Foundation](../03-PrometheusFoundation/README.md) for Prometheus OSS. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
