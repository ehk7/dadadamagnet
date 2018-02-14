import paho.mqtt.client as mqtt
import time
from enum import Enum


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
        client.subscribe("esys/dadada/status")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if msg.topic == "esys/dadada/status":
            self.mainframe.status = int(msg.payload)
            print("STATUS "+str(self.mainframe.status))
            if self.mainframe.status==1:
                self.mainframe.txt2.Label="LOCKED"
            elif self.mainframe.status==2:
                self.mainframe.txt2.Label="CLOSED/UNLOCKED"
            elif self.mainframe.status==3:
                self.mainframe.txt2.Label="OPEN"

    def publish(self, topic, message):
        self.client.publish(topic, message)

if __name__=="__main__":
    mq = MQTTManager()
