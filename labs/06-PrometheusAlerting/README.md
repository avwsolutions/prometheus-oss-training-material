# Introduction lab exercises

Welcome to the Prometheus Alerting lab exercises. Throughout these exercises, participants will engage in a series of practical tasks and activities designed to build hands-on experience and develop key observability skills. Attendees will have the opportunity to explore, experiment, and deepen their understanding of modern observability concepts and practices, with a particular focus on Prometheus.

The goal of these lab exercises is to actively engage with the material and ask questions whenever something is unclear or you encounter a blocker. It is important to note that there are no strict dependencies between the labs, so it is perfectly fine to progress at your own pace, even if you fall behind on a particular exercise.

The following key topics are part of these exercises:

- Setup `Alertmanager`
- Adding alert rules
- Extending the route configuration
- Enabling Slack notification


## Exercise 1 - Setup Alertmanager

This first exercise you are going to learn how to activate `Alertmanager` and create a minimal `Route configuration`. You may already have a service, but requires additional configuration.

> [!NOTE]  
> Since you already are familiar with most concepts like the *container* setup, not every step is fully explained.

### Exercise 1.1 - Activate Alertmanager

The following tasks need to be completed, before you can run the actually job.

Complete the following tasks to update your *prometheus-playground*:

- Ensure that the *alertmanager* service is available in the `compose.yml`.
- You may have seen that the current `alertmanager.yml` configuration only has an *empty placeholder*. You need to create a configuration that fullfills the following requirements.
    - Ensure *Grouping* is by `alertname`.
    - *Group waiting* must set to `30 seconds`.
    - *Group interval* must be `2 minutes`.
    - *Repeat interval* must be `5 minutes`.
    - Complete your configuration with a *default* route to a receiver *default*.
- Ensure that you have registered the *alerting alertmanagers* instance to the `prometheus.yml` configuration file.
- Validate using the `Prometheus UI` is the `Alertmanager` is online and available.

### Exercise 1.2 - Activate a DeadMansSwitch

A *DeadMansSwitch* alert in Prometheus is an alert that is always firing. If Alertmanager stops receiving it, you know something in the monitoring pipeline has broken.

Nice thing of using `vector(1)` that it's always evaluates to a non-zero value, so the alert is always active.

Below an examplw how you can implement this as an `Alert rule`.

```
groups:
  - name: periodic-healthchecks
    rules:
      - alert: DeadMansSwitch
        expr: vector(1)
        for: 1m
        labels:
          severity: none
        annotations:
          summary: "DeadMansSwitch"
          description: "This is an always firing Watchdog alert that reports monitoring pipeline health state!"
```

Complete the following tasks to implement your first *alert rule*.

- Create a new configuration file for `Prometheus` called `alerts.yml`.
- Copy the above code snippet to create your first rule.
- Don't forget to mount the file as `volume` under the `Prometheus` service. Take the `prometheus.yml` as example.
- Ensure that the new rules file called `alerts.yml` is registered under `rule_files` section.
- Now update/restart the containers to pick-up the changes.
- Do you see your first alert appear?
    - What is the current status?
    - Did the status change?
    - What is the final status?
- Lookup the alert in the `Alertmanager UI`.
    - Can you see *Info* fields?
    - Now *snooze* the alert by registering a *silence* for 5 minutes. Provide your own *name* and *comments*.
    - The alert should now we hidden and only visible under *Silences*.

## Exercise 2 - Adding alert rules

This second assignment we are going to implement some more *alert rules*. During the previous exercise you learned about the format. You it should be easy to add another one.

Let's get started!

### Exercise 2.1 -  alerting on host down

Implementing the classic host down can be implemented for registered instances using a special metric called `up`.
Let's implement this alert rule.

Complete the following tasks to implement your the *alert rule*.

- Use a new group called *availability-alerts*.
- Add a single alert definition called *InstanceDown*.
- Use the *expression* when nodes are down, so `up == <fill in the blank>`.
- Set the check to 1 minute.
- Ensure that a *security* of *critical* is added.
- Add two annotations called *summary* and *description*.
    - In summary say *Instance down*.
    - In the description mention the *instance* that is down. The *instance* must be a $label variable to show the actual instance that is reporting downtime.
- Now restart the Prometheus service and validate if the new *alert rule* becomes active.
- To simulate downtime you can stop either the `blackbox-exporter` or `node-exporter`.

### Exercise 2.2 - Work with alert templating

You already have noticed that the *instance* value still contains the *port number*. Within alert rules you can apply simple templating to format the alert labels.This exercise you are going to strip the port number. Another improvement is creating an additional *alert rule* for websites. Let's get started.

Before starting the exercise you may want to consult the [Template Reference](https://prometheus.io/docs/prometheus/latest/configuration/template_reference/).

- Open the `alerts.yml`.
- Split the current alert rule in two rule definitions by using the *job* selector.
- Ensure that you strip the port number.
- Ensure for the new alert rule called *WebsiteMonitorDown*.
    - summary it says - *Website monitor down*.
    - In the description ensure the followeing example is shown, *Website https://example.com is down*
- Are both alerts still grouped together? Explain why.

### Exercise 2.3 - Implement rules for capacity alerting

You now know you to create alert rules, use *simple templating* and this *alert rule* we take it a little step to *advanced templating*.

> [!NOTE]  
> Due to complexity I do recommnend not to use too match advanced templating, so only when needed!

Below the advanced templating script you can use as example. Notice how:

- `$labels` and `$value` are used.
- `Range query` to loop over a `PromQL` query output.
- `Printf` statement to print in percentages.

```
description: |
    Filesystem usage is above 90%.

    Instance: {{ $labels.instance }}
    Device: {{ $labels.device }}
    Mountpoint: {{ $labels.mountpoint }}

    Current usage: {{ printf "%.2f" $value }}

    All filesystems on this host:

    {{ range query (printf `
      100 - (
        node_filesystem_avail_bytes{instance="%s",fstype!~"tmpfs|overlay"} * 100
        / node_filesystem_size_bytes{instance="%s",fstype!~"tmpfs|overlay"}
      )` $labels.instance $labels.instance) }}
    - {{ .Labels.mountpoint }}: {{ printf "%.2f" .Value }}%
    {{ end }}
```

Complete the following tasks to implement your the *alert rule*.

- Ensure that you put this rule under `capacity alerts`.
- Give the alert a name lik `FilesystemUsageHigh`.
- Use your previous created queries at [exercise 4.2](../05-PrometheusQuerying/README.md).
- Ensure that the summary shows `"Filesystem usage high on <system>`.

Start create this filesystemUsageHigh metric. Additionally you could create the same rule for `Inode usage`. Find the correct metric and reuse the alert rule `PromQL` logic.

## Exercise 3 - Extending the route configuration

This exercise we are going to extend the `route configuration`.

### Exercise 3.1 -  Add operations route

Currently the Operations team handles our `critical`  alerts. You should implemented a critical severity for both *InstanceDown* and *WebsiteMonitorDown*.

For this we are going to extend the `alertmanager.yml`. 

The following tasks need to be completed, before they can receive `notifications`.

Complete the following tasks to update your *prometheus-playground*:

- Edit the `alertmanager.yml` configuration. Please take care of the correct annotation.
- Add an additional route with a receiver called `operations`. For the moment use a dummy integration.
- Restart the `Alertmanager` service.
- Now retrigger `any critical alert`.
- Do you notice something? Are the alerts also shown under the `default route`.


### Exercise 3.2 -  Ensure SRE routes

In the previous exercise you have created a `route`.  If there is a match, the match breaks and stops as expected. You as a `SRE` team still want to receive all severity. Let's add the `SRE` route.

- Edit the `alertmanager.yml` configuration. Please take care of the correct annotation.
- Add an additional route with a receiver called `SRE`. For the moment use a dummy integration.
- Ensure that you have added the `continue: true` flag to the `operations` route.
- Restart the `Alertmanager` service.
- Now retrigger `any alert`.
- Do you notice something? Nothing must be shown under `default route` anymore.

### Exercise 3.3 -  Configure a Null rule

You may have asked why this *DeadMansSwitch* alert is comstantly spamming us. It has a reason, but we can implement a time-window, so it's silenced and not send out alerts during office hours. To achieve this you will create a *route: null* likke */dev/null*.

- Edit the `alertmanager.yml` configuration. Please take care of the correct annotation.
- Add an additional route with a receiver called `null`. For the moment use a dummy integration.
- Ensure that this route is on top, so above the `operations` route.
- This `null` route must only match *DeadManSwitch*.
- Now add a a `time_intervals` named `office-hours`. Don't forget to add the `time_intervals`.
    -  weekdays, monday-friday.
    -  times, 9:00 - 17:00.
- Restart the `Alertmanager` service.
- Now retrigger `any alert`.
- Can you now add a `time_intervals`names `outside hours` and ensure the *DeadmanSwitch* alert is end to `operations`?

# exercise 4 - Enabling Slack notification

This bonus exercise you are going to integrate `Slack for SRE`. During this exercise you need either your own `Slack` or `avwsolutions` temporary `api-key`.

## Exercise 4.1 - Setup the Slack integration

As mentioned above, ensure you have the `webhook` available. If you don't have it, just configure it with a `dummy value`.

```
slack_configs: 
      - api_url: "<your webhook>"
        channel: "<#Yourchannel>"
        send_resolved: true
        title: "[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }}"
        text: |
          *Alert:* {{ .CommonLabels.alertname }}
          *Service:* {{ .CommonLabels.service }}
          *Severity:* {{ .CommonLabels.severity }}
          
          {{ range .Alerts }}
          • {{ .Annotations.summary }}
          {{ end }}
```

Complete the following tasks to update your *prometheus-playground*:

- Edit the `alertmanager.yml` configuration. Please take care of the correct annotation.
- Under the receiver called `SRE` add the `slack_configs`, see example above.
- Restart the `Alertmanager` service.
- Now retrigger `any alert`.
- You may now receive alert notifications for `SRE` in Slack. 

## Exercise 4.2 - Ensure the service value is configured

When doing notifcations it's a practice to talk about `services` rather then the `only infrastructure`.
Extend all *alert rules* with a service label. Just pick what you thinks fits the most.

Validate in Slack if the `service` is reported.

## Exercise 4.3 - Using a notification template file

This exercise we are going to move our notification `title` and `message` to a template called `sre-slack.tmpl`.

Complete the following tasks to update your *prometheus-playground*:

- Start with copying [sre-slack.tmpl](./content/templates/sre-slack.tmpl) to your configuration.
- Add the file as volume to the alertmanager service.
- Ensure that the file is readonly and mounted under `/etc/alertmanager/templates`.
- Update the current `title` and `message` values to the variables that are in the template.
    - {{ template "slack.title" . }}'
    - {{ template "slack.text" . }}'
- Restart the `Alertmanager` service.
- Now retrigger `any alert`.
- You may now receive alert notifications for `SRE` in Slack with new layout.

## Next Steps

You are ready to start with the Seventh lab about [Prometheus Visualization](../07-PrometheusVisualization/README.md) for Prometheus Visualization. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
