# dedicated-megamek-container

This repo is to aid in setting up and running a dedicate MegaMek server as a container. The Dockerfile is set to automatically download the latest released version.

## Use a published image

Images are published to the GitHub Container Registry, for amd64 and arm64.
Sentry is enabled on the published images.

```bash
docker run --rm -d -p 2346:2346 -v ./userdata:/app/userdata ghcr.io/megamek/megamek:latest
```

| Tag | What you get |
|-----|--------------|
| `latest`, `core` | The newest Core (stable) release |
| `experimental` | The newest Experimental release |
| `v0.51.00.1` | That exact release. Every release has its own tag |

Your server and your players must run the same MegaMek version, so pin a version tag for a long-running game.

## How the images are built

The `Docker image` workflow runs by itself:

- **Every 3 hours** it looks for a new MegaMek release, Core or Experimental. It builds one only when its image is missing.
- **Every Monday** it builds the current Core and Experimental images again. That picks up Java and Ubuntu security patches.
- **Every build** starts the server and waits for port 2346 before anything is published.

To build by hand, run the workflow from the Actions tab. You can name one release, force a rebuild, or do a dry run that publishes nothing.

## Build the docker container to run dedicated server

```bash
docker build --build-arg MM_VERSION=<version to build> --build-arg SENTRY_ENABLED=<true or false> --tag megamek:<version> .
```

## To build for multiple platforms

```bash
docker buildx build --platform=linux/amd64,linux/arm64  --build-arg MM_VERSION=<version to build> --build-arg SENTRY_ENABLED=<true or false> -t megamek:<version> .
```

## Running the container

We should now have a megamek container built. You can run the container with the following command:

```bash
docker run --rm -d -p 2346:2346 megamek:<version>
```

You should now be able to connect to the above dedicate megamek server on localhost or your LAN IP and port 2346

## Running the container with custom user folders

Create a folder to store all of your custom user data, meks, maps, etc.. Recommend a `userdata` folder
locally. The command below assumes it is created within the folder you're running the command from.
Change the `./userdata` portion to be the path where you wish to have it stored.

```bash
docker run --rm -d -p 2346:2346 -v ./userdata:/app/userdata megamek:<version>
```

## Sentry Configuration

A point of note, this image is configured to allow the enable or disable of Sentry upon build. The published images have Sentry enabled for the MegaMek team to get as much error data as possible. You can disable in your own build by passing `false` to the above build arg.
