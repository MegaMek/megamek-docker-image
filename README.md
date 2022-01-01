# dedicated-megamek-container

This repo is to aid in setting up and running a dedicate megamek server as a container.

Within this folder is an empty `app` folder. Place the decompressed archive from
<https://megamek.org/downloads> inside of it. So if downloading MegaMek-0.47.9.tar.gz,
you would decompress it and copy all files from inside the decompressed folder and place
them inside the app folder. Afterwards, you just build/tag the image and you're good
to go.

## Build the docker continer to run dedicate server

```bash
docker build --tag megamek:<version> .
```

## To build for multiple platforms

```bash
docker buildx build --platform=linux/amd64,linux/arm64 -t tapenvyus/megamek:<version> .
```

## Running the container

We should now have a megamek container built. You can run the container with the following command:

```bash
docker run --rm -d -p 2346:2346 megamek:<version>
```

You should now be able to connect to the above dedicate megamek server on localhost or your LAN IP and port 2346
