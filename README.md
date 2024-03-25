# Spotify MQTT publisher

This MQTT publisher broadcasts information of the song currently playing on Spotify.
The project was developed in **Python 3.11.4**.

This project requires that a eclipse-mosquitto docker container is running before publishing the Spotify's information.

## Create a virtual environment and install the required packages

First, create a virtual environment and then install the packages:
```bash
python3 -m venv ./py-venv
source ./py-venv/bin/activate
pip3 install -r requirements.txt
```

Here is the list with the packages required and the version used for this project:
- dbus-python 1.3.2
- paho-mqtt 2.0.0

For this project we are using the library [mpris2](https://github.com/hugosenari/mpris2) to get the information of the song.

## Run script

Assuming you already have the docker container running and you know its IP address, execute the script with the
following parameters:
```bash
python3 ./spotfiy-mqtt-pub.py --broker 172.18.0.1 --port 1883
```

By default the script is set with **broker = localhost** and **port = 1883**.