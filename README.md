# dedicated-megamek-container
This repo is to aid in setting up and running a dedicate megamek server as a container.

You will need to acquire the archive from Megamek's github page. Currently this is built from the following release:

<https://github.com/MegaMek/megamek/releases/download/v0.46.1/megamek-0.46.1.tar.gz>

Once you have the archive downloaded we need to extract the contents and archive it again removing the leading directory (megamek-0.46.1) so we are only putting the contents in the container. This is so we don't have to make as many changes when updating for future releases. 

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

## Download the megamek softare.

```
wget https://github.com/MegaMek/megamek/releases/download/v0.46.1/megamek-0.46.1.tar.gz
```

## Extract the megamek softare.

```
tar zxvf megamek-0.46.1.tar.gz
```

## Create new archive to be included in the docker build

```
cd megamek-0.46.1
tar zcvf ../dedicated-megamek-container/megamek-0.46.1.tar.gz .
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
