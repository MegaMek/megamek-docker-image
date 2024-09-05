# dedicated-megamek-container

This repo is to aid in setting up and running a dedicate MegaMek server as a container. The Dockerfile is set to automatically download the latest released version.

## Build the docker container to run dedicate server

```bash
docker build --build-arg MM_VERSION=<version to build> --build-arg SENTRY_ENABLED=<true or false> --tag megamek:<version> .
```

## To build for multiple platforms

```bash
docker buildx build --platform=linux/amd64,linux/arm64  --build-arg MM_VERSION=<version to build> --build-arg SENTRY_ENABLED=<true or false> -t tapenvyus/megamek:<version> .
```

## Running the container

We should now have a megamek container built. You can run the container with the following command:

```bash
docker run --rm -d -p 2346:2346 megamek:<version>
```

You should now be able to connect to the above dedicate megamek server on localhost or your LAN IP and port 2346

## Sentry Configuration

A point of note, this image is configured to allow the enable or disable of Sentry upon build. The images provided to Docker Hub have Sentry enabled for the MegaMek team to get as much error data as possible. You can disable in your own build by passing `false` to the above build arg.
