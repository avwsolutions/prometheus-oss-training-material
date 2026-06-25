# Introduction lab exercises

Welcome to the Prometheus Visualization lab exercises. During the lab exercises the student will experiential work through various tasks and activities to gain practical experience and develop new skills. In hands-on learning, attendees are given the opportunity to explore, experiment, and discover knowledge for themselves about the legendary Elastic Stack.

The goal is to get actively engage and ask questions if something is not clear or you are blocked. Important to understand that there are no strong dependencies between labs, so it's okay if you're behind and follow your own pace.

The following key topics are part of these exercises:

- Setup `Grafana` and explore features
- Using aggregated metrics in Grafana
- Import and customize community dashboards
- Setup the classic `Web Console`


## Exercise 1 - Setup Grafana

This first exercise you are going to learn how to activate `Grafana`, create some dashboards and explore `Prometheus` data.

> [!NOTE]  
> Since you already are familiar with most concepts like the *container* setup, not every step is fully explained.

### Exercise 1.1 - Activate Grafana

First you are going to activate `Grafana` as service by adding a container to the `compose.yml`.  Below the config that you need.

```
grafana:
    image: grafana/grafana-oss:${GRAFANA_VERSION}
    container_name: grafana
    restart: ${RESTART_POLICY}
    environment:
      GF_SECURITY_ADMIN_USER: ${GRAFANA_ADMIN_USER}
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
      GF_USERS_ALLOW_SIGN_UP: "false"
    volumes:
      - grafanadata:/var/lib/grafana
      - ./config/grafana/provisioning:/etc/grafana/provisioning
    ports:
      - "${GRAFANA_PORT}:3000"
    depends_on:
      - prometheus
```

Let's start implementing `Grafana` by completing the following tasks.

- Ensure that the *grafana* service is available in the `compose.yml`.
- I already have a `Grafana` configuration available at [grafana](./content/grafana/). You just have to copy it to your `Prometheus playground` and set the correct [datasource url](./content/grafana/provisioning/datasources/prometheus.yml).
- After restarting/updating all docker services, you can access `Grafana OSS` at `127.0.0.1:3000`.
- You can login with the default credentials, which are `admin:admin`.

### Exercise 1.2 - Explore Grafana

Here we are going to explore Grafana. It's not an indepth Grafana course, so we only focus on `Grafana OSS` features.

Now answer the following questions:
- Where can you find the configured Prometheus connection?
- Which drilldown can you use to look into Prometheus data?
- Are the current alerts managed through Grafana or Alertmanager?
- Lookup the *crm_processing_code* for *customer foobar*, save the query to a panel and create a new dashboard.


## Exercise 2 - Using aggregated metrics in Grafana

### Exercise 2.1 - Create a set of recording rules

Complete the following tasks to implement your first *recording rule*.

- Create a new configuration file for `Prometheus` called `recordings.yml`.
- Copy the following example [recordings.yml](./content/recording-rules/recordings.yml).
- Don't forget to mount the file as `volume` under the `Prometheus` service. Take the `prometheus.yml` as example.
- Ensure that the new rules file called `recordings.yml` is registered under `rule_files` section.
- Now update/restart the containers to pick-up the changes.
- Lookup the user-defined metrics in the `Prometheus UI`.
    - Can you query them?
    - Do you recognise the naming?

### Exercise 2.2 - Create your awesome dashdboard with aggregated metrics

This last exercise ( if you skip the bonus :)  you are going to use the previous created *aggregated metrics* to create panels for them and store them in your *Awesome dashboard*.

I do think the actual *metric* names you can get from the recordings and Grafana will guide you through the setup.

Share the result with the other participants.

### Bonus Exercise 2.3 - Create your own Service-Level Objectives

This exercise you can add how own `SLO`. You may remember the format. Below an example `SLI` query.

Availability of your `node-exporter`
```
sum_over_time(up{job="node-exporter", instance="node-exporter:9100"}[30d]) / count_over_time(up{job="node-exporter", instance="node-exporter:9100"}[30d])
```

CPU Saturation (exlcuding *iowait*.)
```
sum(rate(node_cpu_seconds_total{mode!="idle", mode!="iowait"}[5m])) / sum(rate(node_cpu_seconds_total[5m]))
```

Example alert.

```
groups:
- name: node_slo_alerts
  rules:
  - alert: NodeAvailabilityHighBurn
    expr: sum(rate(up{job="node_exporter"}[1h])) < 0.999 * 14.4
    for: 10m
    labels:
      severity: critical
```
Complete the following tasks:

- Implement the node-exporter SLO.
- Take the SLO value you picked during the first lab.

## Exercise 3 - Import and customize community dashboards

This exercise you are going to reuse community created dashboards. Sometimes it's faster  and more efficient to reuse good dashboards as a template to adjust for your needs.

### Exercise 3.1 - Find and import a dashboard

Open [Grafana Dashboard Community site](https://grafana.com/grafana/dashboards/) and search for a `Node Exporter` dashboard you like. You may want to read the releases and documentation.

The only task here is to copy the *Dashboard ID*.

Now open your Grafana instance and complete the following tasks:
- Open Dashboards.
- Click *New* and choose *Import*.
- Just provide the *Dashboard ID* from the previous step and click *Load* and *Import*.

Now it's time to adjust it for your needs.

### Exercise 3.2 - Adjust the dashboard

As said it's all yours, be creative and share your *Awesome dashboard* with us!

## Bonus Exercise 4 - Setup the classic `Web Console`

This last bonus exercise is setting up the `Web Console`. I have the [Sample templates, static content and Libraries](./content/prometheus-ui-consoles/) for you.

- Ensure that you set the correct startup parameters. You may need `--web.user-assets` for static content.
- If things are not working, ensure to rename `node` to `node-exporter`.
- Did you set the required startup parameters to load the `templates` and `libraries`?

Success with the puzzle!


## Next Steps

You are ready to start with the Eight lab about [Prometheus HA](../08-PrometheusHA/README.md) for Prometheus High Availability and scaling. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
