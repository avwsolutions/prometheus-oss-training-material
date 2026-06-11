# Introduction lab exercises

Welcome to the Prometheus Instrumentation lab exercises. Throughout these exercises, participants will engage in a series of practical tasks and activities designed to build hands-on experience and develop key observability skills. Attendees will have the opportunity to explore, experiment, and deepen their understanding of modern observability concepts and practices, with a particular focus on Prometheus.

The goal of these lab exercises is to actively engage with the material and ask questions whenever something is unclear or you encounter a blocker. It is important to note that there are no strict dependencies between the labs, so it is perfectly fine to progress at your own pace, even if you fall behind on a particular exercise.

The following key topics are covered throughout these exercises:

- Extending the Node Exporter configuration
- Work with the Blackbox Exporter
- Implement a textfile collector 

## Exercise 1 - Extending the Node Exporter configuration

This exercise you are going to extend the existing `Node Exporter` with additional configurationt to learn about the various ways of collecting system metrics. In short the `Node Exporter` is a metric collector that exports both machine hardware and OS metrics and makes them available for *Prometheus Scraping*.

Default not all metrics are collected, for example `sysctl` or `perf`.  During the following tasks you learn howto to add additional collections like `sysctl`.

> [!NOTE]  
> You can use your earlier create prometheus playground. I also have a new copy available.

### Exercise 1.1 - Adding a Sysctl configuration as Info metric

- Find the `node_exporter` service in the `compose.yml`. Now update the node-exporter container with `docker compoose up -d`.
- Add the following flag to the collector startup parameters. Ensure to add the correct indentation and brackets for the compose structure.

```
--collector.sysctl
--collector.sysctl.include-info=vm.swappiness
```
- Look if a metric called *swappiness* does exist. Can you find it and is the value what you expected?

It's avaiable under **node_sysctl_info**, but you also use the `Node Exporter` visit the ['/metrics' endpoint](http://127.0.0.1:9100/metrics).

```
node_sysctl_info
```

Analyze the output of the expression. Using `Info`flag provides a `value` as Info Metric. This is helpful when you want to monitor if a certain parameter exist. In this exercise this isn't what we want to collect for now. Let's update the flags.

### Exercise 1.2 - Adding a Sysctl configuration as numeric metric

Since `swappiness` has a numeric value we can add this as a real `numeric` metric.

- Let's update the flag again by the replacing your previous changes. In essence you have to remove the '-info' part.

```
--collector.sysctl
--collector.sysctl.include=vm.swappiness
```

Now try again and  you will find a new metric called `node_sysctl_vm_swappiness` which provides the actual numeric value as metric. Which type of metric is it?

If you want to learn more about `Node Exporter` just read the [Github documentation](https://github.com/prometheus/node_exporter/).

## Exercise 2 - Work with the Blackbox Exporter

This exercise you will configure the `Blackbox Exporter`. It's helpful when measuring websites or API endpoints for their `HTTP` status code. As you may have seen the `Blackbox Exporter` is already part of the compose.yml and provides an empty placeholder.

### Exercise 2.1 - Setup modules

We are going to configure the actual module that we are going to consume. It's a module called *http_2xx*. This module helps to catch the 'http status` codes like [2xx, 3xx 4xx or 5xxx]. 

Configuration is setup to:
- Test against *http*.
- Timeout of 5 seconds.
- We test for a valid *HTTP_VERSION*.
- Our probe with send out an *GET* for simplicity.
- We prefer using `ipv4` stack.

Below the configuration which you can add to the `blackbox.yml`. This configuration is located under `config/exporters`. 

```
modules:
  http_2xx:
    prober: http
    timeout: 5s

    http:
      valid_http_versions:
        - HTTP/1.1

      method: GET
      preferred_ip_protocol: ip4
```

If you added the configuration you can restart the `Blackbox Exporter` and valide it's available using the [metrics endpoint](http://127.0.0.1:9115/metrics).

### Exercise 2.2 - Adding scraping job

You may have noticed that the *static target* is not yet available. This is something we still have to add to the Prometheus Server configuration. This configuration will actually contain the *probe targets* and requires you to do some additional *relabeling*. This is esential to configure the `Blackbox Exporter`.

Let's add the configuration.

```
 - job_name: blackbox-http
    metrics_path: /probe
    params:
      module:
        - http_2xx
    static_configs:
      - targets:
          - https://example.com
          - https://prometheus.io
        labels:
          app: "blackbox-exporter"
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target

      - source_labels: [__param_target]
        target_label: instance

      - target_label: __address__
        replacement: blackbox-exporter:9115
```

After adding the configuration to the *prometheus.yml* you will see the target to become available. See [Target health](http://127.0.0.1:9090/targets).

Now you have implemented the *instrumentation*. Let's look for the metrics. Multiple metrics are available as **probe_http__**.
Answer the following questions:
- Wat are the current website codes?
- What is the average *rate* over the last *5 minutes* of the probe duration (in seconds).

### Exercise 2.3 - Simulate other http codes

This exercise you going extend the current blackbox configuration that it supports **HTTP/2.0**. Next to this we are going to introduce two failing jobs for later purpose.

Complete the following tasks:
- Ensure that **HTTP/2.0** is added to the list of *valid_http_versions*. This is done using the *blackbox.yml*.
- Add a second job called *service-unavailable-http*. Take the previous scraping job as example, but ensure you scrape the following targets.
  - https://302.returnco.de
  - https://500.returnco.de

Ensure you have updated and restarted Prometheus to pickup the configuration and validate using the **probe_http__** metrics if the actual returned code is what you expect.

## Exercise 3 - implement a textfile collector

This last exercise you get introduced in using the `Textfile collector`. It's an helpful collector when you have applications that can write their own metrics to a *.prom* file.

For example we use a script called [localApp.sh](./content/localApp.sh) you can use to generate the metrics.

### Exercise 3.1 - Configure the Node Exporter

The node exporter doesn't enable textfile collector by default. You have to enable it during startup. Let's update the `compose.yml` again. Also since we work with containers we have to mount the local *textfile_collector* to the container.

Add the following volume to the `Node Exporter` service. Ensure that `config/exporters/textfile_collector` exists.

```
- ./config/exporters/textfile_collector:/var/lib/node_exporter/textfile_collector/:ro
```

Also at the `Node Exporter` service. Ensure this is part of the *command* section.

```
--collector.textfile.directory=/var/lib/node_exporter/textfile_collector/

```

### Exercise 3.2 - Running the script to generate metrics

You may want to run the script or just copy the following to a file called `localApp.prom`.

```
# HELP crm_processing_time Processing time in milliseconds
# TYPE crm_processing_time gauge
crm_processing_time_milliseconds{role="processing-host",customer="foobar"} 125

# HELP crm_processing_status_code Processing status code
# TYPE crm_processing_status_code gauge
crm_processing_status_code{role="processing-host",customer="foobar"} 200

# HELP crm_processing_customer_info Customer information metric
# TYPE crm_processing_customer_info gauge
crm_processing_customer_info{role="processing-host",customer="foobar"} 1
```

If you configured the textfile collector correctly these will show up in Prometheus.

## Next Steps

You are ready to start with the next lab about [Prometheus Querying](../05-PrometheusQuerying/README.md) for Prometheus OSS. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
