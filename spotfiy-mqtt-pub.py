import time
import argparse
import sys
from paho.mqtt import client as mqtt_client
from mpris2.mpris2 import player, interfaces
from mpris2.mpris2.types import Metadata_Map
from dbus.exceptions import DBusException

#------------------------------------------------------------------------------
# MPRIS2 helper functions and variables:
#------------------------------------------------------------------------------

# Variables
#------------------------------------------------------------------------------

spotify_bus_name = f"{interfaces.Interfaces.MEDIA_PLAYER}.spotify"

# Try to open the Spotify's interface. In case is not possible catch the error and
# close the program.
try:
    spotify_player = player.Player(dbus_interface_info={'dbus_uri': spotify_bus_name})
except DBusException as dbus_exception:
    print("Spotify app not running.")
    print(f"{str(dbus_exception.get_dbus_name())}: {str(dbus_exception.get_dbus_message())}")
    sys.exit(1)

# Functions
#------------------------------------------------------------------------------

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

# Default values for the MQTT client
broker = "localhost"
port = 1883
client_id = "spotify-pub"

# Spotify's MQTT topics
main_topic = "spotify"
metadata_topic = f"{main_topic}/metadata"
# track_title is a string type
track_title_topic = f"{metadata_topic}/title"
# album_name is a string type
album_name_topic = f"{metadata_topic}/album"
# track_artist is a string type
track_artist_topic = f"{metadata_topic}/artist"

# Callback functions for mqtt client
#------------------------------------------------------------------------------

def on_connect_cbk(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to {client.host} with reason code: {reason_code}")
    else:
        print(f"Failed to connect, return code: {reason_code}\n")
    
def on_disconnect_cbk(client, userdata, flags, reason_code, properties):
    print(f"Disconnected from {client.host} with reason code: {reason_code}.")

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

#------------------------------------------------------------------------------
# Util functions:
#------------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker', type=str, default=broker)
    parser.add_argument('--port', type=int, default=port)
    parser.add_argument('--id', type=str, default=client_id)
    return parser.parse_args()

#------------------------------------------------------------------------------
# Main loop:
#------------------------------------------------------------------------------

def run_publisher():
    cmd_args = parse_args()
    _broker = cmd_args.broker
    _port = cmd_args.port
    _client_id = cmd_args.id

    client = connect_mqtt(mqtt_broker=_broker, mqtt_port=_port, mqtt_client_id=_client_id)
    print("To exit press Ctrl+c")

    try:
        while True:
            spotify_metadata = get_metadata_from_player()

            client.publish(track_title_topic, spotify_metadata[0])
            client.publish(album_name_topic, spotify_metadata[1])
            client.publish(track_artist_topic, spotify_metadata[2])

            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\nExiting...")

    client.disconnect()
    
if __name__ == '__main__':
    run_publisher()