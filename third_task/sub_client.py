import paho.mqtt.client as paho
from paho import mqtt
import os


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload.encode('utf-8')))


client = paho.Client(client_id="SUB Client", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
client.connect(os.getenv('MQTT_BROKER'), 8883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


try:
    client.subscribe("itis/team_9/led/color")
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print('Shutdown. Client disconnected')
