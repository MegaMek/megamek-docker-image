# dedicated-megamek-container
This repo is to aid in setting up and running a dedicate megamek server as a container.

Within the Dockerfile there is a URL for the release you want to build. I will eventually create a variable for the version.

 Currently this is built from the following release:

<https://github.com/MegaMek/megamek/releases/download/v0.46.1/megamek-0.46.1.tar.gz>

You can build any release by updating the download URL in the Dockerfile.

I am a Linux users so here are the steps I have used to build this container. If you are on some other OS, YMMV.

I am assuming you have Docker installed.

## Create build space

```
mkdir buildspace; cd buildspace
```

## Clone repo for building container

```
git clone git@github.com:andrewjkrull/dedicated-megamek-container.git
```

## Build the docker continer to run dedicate server

```
cd ../dedicated-megamek-container
docker build --tag megamek:0.46.1 .
```

## Running the container
We should now have a megamek container built. You can run the container with the following command:

```
docker run --rm -d -p 2346:2346 megamek:0.46.1
```
You should now be able to connect to the above dedicate megamek server on localhost or your LAN IP and port 2346
