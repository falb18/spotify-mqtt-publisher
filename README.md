# Spotify MQTT publisher

This MQTT publisher broadcasts information of the track currently playing on Spotify.
The project was developed with **Python 3.11.4**.

This project requires an eclipse-mosquitto docker container running before publishing the current track information playing.
Here are some useful links that explained how to create, configure and run the eclipse-mosquitto container:
- [Running The Mosquitto MQTT Broker In a Docker Container](http://www.steves-internet-guide.com/running-the-mosquitto-mqtt-broker-in-docker-beginners-guide/)
- [Instalación de Mosquitto (MQTT Broker) en Docker](https://www.manelrodero.com/blog/instalacion-de-mosquitto-mqtt-broker-en-docker)

## Create a virtual environment and install the required packages

First, create a virtual environment and then install the packages:

```bash
python3 -m venv ./py-venv
source ./py-venv/bin/activate
pip3 install -r requirements.txt
```

Here are the packages and their version used in this project:
- dbus-python 1.3.2
- paho-mqtt 2.0.0

For this project we are using the library [mpris2](https://github.com/hugosenari/mpris2) to get the track's information.
However, ths library is not listed in the python packages so the repo is cloned as a submodule. You can initialize it with
the following command:

```bash
git submodule add https://github.com/hugosenari/mpris2
```

## Run script

You need to setup a MQTT broker, in my case a use a eclipse-mosquitto docker container that handles the topics.
Execute the script with the following parameters, modify the IP address to match your broker's IP address:

```bash
python3 spotify-mqtt-pub.py --broker 172.18.0.1 --port 1883
```

If the script is executed without arguments then the defautlt values are taken, which are: **broker = localhost** and
**port = 1883**.

## Topics

Here is the list of topics published by this client:
- spotify/metadata/title
- spotify/metadata/album
- spotify/metadata/artist