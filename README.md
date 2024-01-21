# dedicated-megamek-container

This repo is to aid in setting up and running a dedicate MegaMek server as a container. The Dockerfile is set to automatically download the latest released version.

## Build the docker container to run dedicate server

```bash
docker build --build-arg MM_VERSION=<version to build> --tag megamek:<version> .
```

## To build for multiple platforms

```bash
docker buildx build --platform=linux/amd64,linux/arm64  --build-arg MM_VERSION=<version to build> -t tapenvyus/megamek:<version> .
```

## Running the container

We should now have a megamek container built. You can run the container with the following command:

```bash
docker run --rm -d -p 2346:2346 megamek:<version>
```

You should now be able to connect to the above dedicate megamek server on localhost or your LAN IP and port 2346
