import paho.mqtt.client as mqtt
import time
from enum import Enum
from json import loads

class Status(Enum):
    UNCALIBRATED = 1
    CALIBRATING = 2
    LOCKED = 3
    CLOSED = 4
    OPEN = 5


class MQTTManager:
    def __init__(self, mainframe):

        self.mainframe=mainframe
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("192.168.0.10", 1883, 60)
        print("connected")
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("esys/time")
        #client.subscribe("esys/dadada/status")

        client.subscribe("esys/dadada/userstatus")
        client.subscribe("esys/dadada/status2")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if msg.topic=="esys/dadada/status":
            data = loads(msg.payload)
            if data["Door state"]=='Calibratedaaaaaaaaaaaaaaaaaaa' or data["Door state"]=="Waiting for calibration" or data["Door state"]=="Calibrated":
                return 0
            self.doorstate = data["Door state"]
            self.timestamp = data["Time Stamp"]
            self.mainframe.DisplayStatus(str(self.doorstate))


    def publish(self, topic, message):

        self.client.publish(topic, bytes(message, 'utf-8'))
