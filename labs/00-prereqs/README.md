# Initial setup prerequisites

Welcome to the Intial setup prerequisites. During the lab exercises the student will experiential work through various tasks and activities to gain practical experience and develop new skills. In hands-on learning, attendees are given the opportunity to explore, experiment, and discover knowledge for themselves about setting up a development environment for Prometheus-Grafana-Otel Playground.

The goal is to get actively engage and ask questions if something is not clear or you are blocked. Important to understand that there are no strong dependencies between labs, so it's okay if you're behind and follow your own pace.

The following key topics are part of these exercises:

- containerization prerequisites
- Setup Podman Desktop
- Install supporting Tools
  
## Exercise 1 - Validate your containerization prerequisites

This exercise helps you to setup containerization. Most cases you will use a Container Orchestration tool, such as `Kubernetes`. Container workloads are easy to deploy, scale and provide a good way of isolating application services. During the exercises we wil use a Podman (instead of VMWare) setup. Additionally ensure that `Virtualization Technology support` is enabled in the System BIOS.

For Windows users, don't forget to setup Windows Subsystem Layer (WSL2). You can follow the instructions at [Microsoft Learn WSL Setup](https://learn.microsoft.com/en-us/windows/wsl/install-manual).

## Exercise 2 - Setup Podman Desktop

Installation is really straightforward, but be aware of above notes. You may want to download the installer from [Podman.IO](https://podman.io/). Ensure you have `Docker Compatibility` enabled.  For more installation support read the [Podman Installation Instructions](https://podman.io/docs/installation).

When you join a classroom training, you are lucky, since I've already setup Podman Desktop for you.

### 2.2 - Create docker Symbolic Link

it's good to create a *SymbolicLink* for `docker` to the `podman` executable.

For Windows using PowerShell

```
cd C:\Program files\RedHat\Podman
New-Item -ItemType SymbolicLink -Path "docker.exe" -Target "C:\Program files\RedHat\Podman\podman.exe"
```

## Exercise 3 - Install supporting Tools

Most excises require development skills. That's why it's good to prepare your environment with the following development tools.

- Git - SCM tool for cloning versionized repositories from Github.
- Optional - VS Code - Your free IDE Editor.
- Optional - PowerShell 7 - Just better and improved for Linux.

### 3.1 - Install Git SCM

```
winget install --id=Git.Git  -e
```

### 3.2 - Optional - Install Sysmon

```
winget install --id=Microsoft.Sysinternals.Sysmon  -e
```

### 3.3 - Optional - Install VS Code

```
winget install --id=Microsoft.VisualStudioCode  -e
```
### 3.4 - Optional - Install PowerShell 7

```
winget install --id=Microsoft.PowerShell  -e
```

## Next Steps

You are ready to start with the next lab about [Observability Primer](../01-ObservabilityPrimer/README.md). Be aware that the trainer might have to explain the training material and provide additional instructions for a jump start.

Enjoy the exercises!!!

