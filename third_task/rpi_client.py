import paho.mqtt.client as paho
from paho import mqtt
import os
import RPi.GPIO as GPIO
from pirc522 import RFID
import time


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="RPI Client", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
client.connect(os.getenv('MQTT_BROKER'), 8883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

current_color = None
try:
    GPIO.setmode(GPIO.BOARD)
    greenLedPin = 11
    blueLedPin = 13
    GPIO.setup(greenLedPin, GPIO.OUT, initial=0)
    GPIO.setup(blueLedPin, GPIO.OUT, initial=0)
    RFID_UID = [170, 33, 136, 22, 21]
    rc522 = RFID()
    while True:
        rc522.wait_for_tag()
        (error, tag_type) = rc522.request()

        if not error:
            (error, uid) = rc522.anticoll()

            if not error:
                if RFID_UID == uid:
                    GPIO.output(blueLedPin, GPIO.LOW)
                    GPIO.output(greenLedPin, GPIO.HIGH)
                else:
                    GPIO.output(greenLedPin, GPIO.LOW)
                    GPIO.output(blueLedPin, GPIO.HIGH)

                if current_color is not None:
                    client.publish('itis/team_9/led/color', f'Color changed to: {current_color}')

                time.sleep(1)

except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except Exception:
    print("Other Exception")
finally:
    client.disconnect()
    GPIO.cleanup()
    print("End of program")
