import time
import argparse
from paho.mqtt import client as mqtt_client
from mpris2.mpris2 import player, interfaces
from mpris2.mpris2.types import Metadata_Map

# MPRIS2 helper functions and variables
#------------------------------------------------------------------------------

spotify_bus_name = f"{interfaces.Interfaces.MEDIA_PLAYER}.spotify"
spotify_player = player.Player(dbus_interface_info={'dbus_uri': spotify_bus_name})

def get_metadata_from_player() -> None:
    if spotify_player.PlaybackStatus == "Playing" or spotify_player.PlaybackStatus == "Paused":
        print("Current track information:")
        print(f"  Title:  {spotify_player.Metadata[Metadata_Map.TITLE]}")
        print(f"  Album:  {spotify_player.Metadata[Metadata_Map.ALBUM]}")
        # Dbus Array of strings, we need the first element for the artist's name
        print(f"  Artist: {spotify_player.Metadata[Metadata_Map.ARTIST][0]}")

    None

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_client_id = "spotify-pub"
topic = "spotify/"

# Callback functions for mqtt client
#------------------------------------------------------------------------------

def on_connect_cbk(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to {client.host} with reason code: {reason_code}")
    else:
        print(f"Failed to connect, return code: {reason_code}\n")
    
def on_disconnect_cbk(client, userdata, flags, reason_code, properties):
    print(f"Disconnected from {client.host} with reason code: {reason_code}.")

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

def run_publisher():
    cmd_args = parse_args()
    mqtt_client = cmd_args.broker
    mqtt_client = cmd_args.port

    client = connect_mqtt()
    print("To exit press Ctrl+c\n")

    try:
        count = 0
        while True:
            get_metadata_from_player()
            message = f"Test message {count}"
            client.publish(topic, message)
            print(f"Published: {message}")
            time.sleep(5)
            count += 1
    
    except KeyboardInterrupt:
        print("Exiting...")

    client.disconnect()
    
if __name__ == '__main__':
    run_publisher()