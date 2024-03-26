# The purpose of this module is to test the messages published by spotify-mqtt-pub.py

import sys
import argparse
from paho.mqtt import client as mqtt_client

#------------------------------------------------------------------------------
# Spotify MQTT subscriber:
#------------------------------------------------------------------------------

# Default values for the MQTT client
broker = "localhost"
port = 1883
client_id = "spotify-sub"

# Spotify's MQTT topics
main_topic = "spotify"
metadata_topic = f"{main_topic}/metadata"
# track_title is a string type
track_title_topic = f"{metadata_topic}/track_title"
# album_name is a string type
album_name_topic = f"{metadata_topic}/album_name"
# track_artist is a string type
track_artist_topic = f"{metadata_topic}/track_artist"

spotify_topics = [(track_title_topic, 0), (album_name_topic, 0), (track_artist_topic, 0)]

# Callback functions for mqtt client
#------------------------------------------------------------------------------
def on_connect_cbk(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to {client.host} with reason code: {reason_code}")
    else:
        print(f"Failed to connect, return code: {reason_code}\n")
        sys.exit(1)
    
def on_disconnect_cbk(client, userdata, flags, reason_code, properties):
    print(f"Disconnected from {client.host} with reason code: {reason_code}.")

def on_message_cbk(client, userdata, msg):
        print(f"Topic: {msg.topic}\nMessage: {msg.payload.decode()}")

# Functions
#------------------------------------------------------------------------------

def connect_mqtt(mqtt_broker, mqtt_port, mqtt_client_id) -> mqtt_client.Client:    
    client = mqtt_client.Client(
                client_id=mqtt_client_id,
                callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2
            )
    client.on_connect = on_connect_cbk
    client.on_disconnect = on_disconnect_cbk
    client.connect(mqtt_broker, mqtt_port)
    return client

def subscribe(mqtt_client, mqtt_topics) -> None:
    mqtt_client.subscribe(mqtt_topics)
    mqtt_client.on_message = on_message_cbk


#------------------------------------------------------------------------------
# Main loop:
#------------------------------------------------------------------------------

def main(opt):
    _broker = opt.broker
    _port = opt.port
    _id = opt.id

    mq_client = connect_mqtt(_broker, _port, _id)
    subscribe(mq_client, spotify_topics)
    mq_client.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")

    mq_client.loop_stop()
    mq_client.disconnect()

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker', type=str, default=broker)
    parser.add_argument('--port', type=int, default=port)
    parser.add_argument('--id', type=str, default=client_id)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main(arg_parser())