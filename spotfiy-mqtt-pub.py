import time
import argparse
from paho.mqtt import client as mqtt_client
from mpris2.mpris2 import player, interfaces
from mpris2.mpris2.types import Metadata_Map

#------------------------------------------------------------------------------
# MPRIS2 helper functions and variables:
#------------------------------------------------------------------------------

spotify_bus_name = f"{interfaces.Interfaces.MEDIA_PLAYER}.spotify"
spotify_player = player.Player(dbus_interface_info={'dbus_uri': spotify_bus_name})

def get_metadata_from_player() -> list:
    metadata = list()
    if spotify_player.PlaybackStatus == "Playing" or spotify_player.PlaybackStatus == "Paused":
        metadata.append(spotify_player.Metadata[Metadata_Map.TITLE])
        metadata.append(spotify_player.Metadata[Metadata_Map.ALBUM])
        # Dbus Array of strings, we need the first element for the artist's name
        metadata.append(spotify_player.Metadata[Metadata_Map.ARTIST][0])
    
    return metadata


#------------------------------------------------------------------------------
# Spotify MQTT publisher:
#------------------------------------------------------------------------------

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_client_id = "spotify-pub"

# Spotify's MQTT topics
main_topic = "spotify"
metadata_topic = f"{main_topic}/metadata"
# track_title is a string type
track_title_topic = f"{metadata_topic}/track_title"
# album_name is a string type
album_name_topic = f"{metadata_topic}/album_name"
# track_artist is a string type
track_artist_topic = f"{metadata_topic}/track_artist"

# Callback functions for mqtt client
#------------------------------------------------------------------------------

def on_connect_cbk(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to {client.host} with reason code: {reason_code}")
    else:
        print(f"Failed to connect, return code: {reason_code}\n")
    
def on_disconnect_cbk(client, userdata, flags, reason_code, properties):
    print(f"Disconnected from {client.host} with reason code: {reason_code}.")

# Functions:
#------------------------------------------------------------------------------

def connect_mqtt():
    client = mqtt_client.Client(
                client_id=mqtt_client_id,
                callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2
            )

    client.on_connect = on_connect_cbk
    client.on_disconnect = on_disconnect_cbk
    client.connect(mqtt_broker, mqtt_port)
    return client

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker', type=str, default=mqtt_broker)
    parser.add_argument('--port', type=int, default=mqtt_port)
    return parser.parse_args()

# Main loop:
#------------------------------------------------------------------------------

def run_publisher():
    cmd_args = parse_args()
    mqtt_client = cmd_args.broker
    mqtt_client = cmd_args.port

    client = connect_mqtt()
    print("To exit press Ctrl+c\n")

    try:
        while True:
            spotify_metadata = get_metadata_from_player()

            client.publish(track_title_topic, spotify_metadata[0])
            client.publish(album_name_topic, spotify_metadata[1])
            client.publish(track_artist_topic, spotify_metadata[2])

            time.sleep(5)
    
    except KeyboardInterrupt:
        print("Exiting...")

    client.disconnect()
    
if __name__ == '__main__':
    run_publisher()