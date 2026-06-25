# Introduction lab exercises

Welcome to the Prometheus HA lab exercises. During the lab exercises the student will experiential work through various tasks and activities to gain practical experience and develop new skills. In hands-on learning, attendees are given the opportunity to explore, experiment, and discover knowledge for themselves about the legendary Elastic Stack.

The goal is to get actively engage and ask questions if something is not clear or you are blocked. Important to understand that there are no strong dependencies between labs, so it's okay if you're behind and follow your own pace.

The following key topics are part of these exercises:

- Setup Federated Prometheus
- Run Prometheus in Agent-Mode
- Enable Service Discovery

# Exercise 1 - Setup Federated Prometheus

> [!NOTE]  
> Since you should be familiar with most concepts like the *container* setup and *Prometheus configuration*, not every step is fully explained.

This first exercise you are going to learn how to setup `Federated Prometheus`. In short you introduce a second `Prometheus` instance, which receives metrics at an `Edge` location and gets scraped by the `Central Prometheus`.

- Configure the `component.yml`  in your `Prometheus Playground`. Use [compose.yml](./content/compose.yml) as example.
- Ensure that you have configured the `Federated Prometheus`, see [config snippet](./content/config/prometheus-federated/).
- Ensure you have added the '/federate' scrape job at the `Central Prometheus`.


## Exercise 2 - Run Prometheus in Agent-Mode

> [!NOTE]  
> Since you should be familiar with most concepts like the *container* setup and *Prometheus configuration*, not every step is fully explained.


This second exercise you are going to learn how to setup `Prometheus Agent`. In short you introduce a third `Prometheus` instance, which only-scrapes metrics at an `Edge` location and forwards them to the  `Federated Prometheus`.

- Configure the `component.yml`  in your `Prometheus Playground`. Use [compose.yml](./content/compose.yml) as example.
- Ensure that you have configured the `Prometheus Agemt`, see [config snippet](./content/config/prometheus-agent//).
- To validate everything you can spin-up a second `Node-Exporter` called *node-exporter2*.

### Bonus Exercise 3 - Enable Service Discovery

Last exercise is enabling `Docker based` discovery. Take a look at the documentation and configure this in a `Prometheus Instance`.

See the example below for Linux and WIndows.

```
unix:///run/docker/docker.sock
```
```
'npipe:////./pipe/docker-default'
```

## Next Steps

You are ready to start with the Ninth lab about [Prometheus Administration](../09-PrometheusAdmin/README.md) for Prometheus Administration and troubleshooting. Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!
