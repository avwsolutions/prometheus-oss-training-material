# Introduction lab exercises

Welcome to the Prometheus Administration and Troubleshooting lab exercises. Throughout these exercises, participants will engage in a series of practical tasks and activities designed to build hands-on experience and develop key observability skills. Attendees will have the opportunity to explore, experiment, and deepen their understanding of modern observability concepts and practices, with a particular focus on Prometheus.

The goal of these lab exercises is to actively engage with the material and ask questions whenever something is unclear or you encounter a blocker. It is important to note that there are no strict dependencies between the labs, so it is perfectly fine to progress at your own pace, even if you fall behind on a particular exercise.

The following key topics are part of these exercises:

- Creating snapshots
- Restoring snapshot

## Exercise 1 - Creating snapshots

This first exercise you are going to learn how to active the `admin-api` and create a `snapshot` for future recovery purposes.

> [!NOTE]  
> Since you already are familiar with most concepts like the *container* setup, not every step is fully explained.

### Exercise 1.1 - Activate Admin API

First you need to activate the `admin-api` by adding this as startup parameter to the `prometheus` service in the `compose.yml` file.

Let's activate the endpoint by completing the following tasks.

- Open the `compose.yml` and look for the `Prometheus` service.
- Add the flag `-web.enable-admin-api` to the startup parameters.
- Ensure that you know/write down the `tsdb.path`. Here is where the `snapshots` folder is stored.
- After restarting/updating all docker services, you can access the `admin-api`.
- Try to `GET` the endpoint on `http://prometheus:9090/api/v1/features` and look if the `admin-api` is enabled.

## Exercise 1.2 - Create snapshot

Creating snapshots is really easy. It's just a `API` call to the Admin REST Interface. You can either use `PUT` or `POST`. I prefer `POST`.

Now answer the following questions:
- Compose the `POST` command and create a snapshot.
- Did the snapshot succeeded, see the response.
- Lookup the snapshots located in the actual `Prometheus` container using `docker exec -it prometheus sh`.

## Exercise 1.3 - Restore snapshot

Try to restore your previous snapshot by mounting your `snapshot` as `tsdb.location`.

> Warning:
> On your risk, since you could corrupt your `running` environment.

## Next Steps

You have successfully completed all labs for the Prometheus OSS training course. You are now ready to enter the real world and create awesome Prometheus OSS Stack!

Still not enough?
Enjoy the optional [Capture the Bug Challenge](../99-CapturetheBug/README.md).
