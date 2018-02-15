"""
MQTTManager class, used to manage mqtt communication with the device
"""
import paho.mqtt.client as mqtt
import time
from enum import Enum
from json import loads

class Status(Enum):
    """
    Enum subclass representing the states of the lock
    """
    UNCALIBRATED = 1
    CALIBRATING = 2
    LOCKED = 3
    CLOSED = 4
    OPEN = 5


class MQTTManager:
    """
    Handles MQTT communication
    """
    def __init__(self, mainframe, broker="192.168.0.10", port=1883):
        """
        Sets up an MQTT instance, including connecting to the broker
        :param mainframe:
        :param port: the port to connect to to
        :param broker: the broker address to connect to
        """
        self.mainframe=mainframe
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(broker, port, 60)
        print("connected")
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        Event handler for succesful connection to broker. Subscribes to several topics.
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return: no return value
        """
        print("Connected with result code " + str(rc))
        client.subscribe("esys/time")
        #client.subscribe("esys/dadada/status")

        client.subscribe("esys/dadada/userstatus")
        client.subscribe("esys/dadada/status2")

    def on_message(self, client, userdata, msg):
        """
        Event handler for when a message is received
        :param client:
        :param userdata:
        :param msg: the message received
        :return: no return value
        """
        print(msg.topic + " " + str(msg.payload))
        if msg.topic=="esys/dadada/status":
            data = loads(msg.payload)
            if data["Door state"]=='Calibratedaaaaaaaaaaaaaaaaaaa' or data["Door state"]=="Waiting for calibration" or data["Door state"]=="Calibrated":
                return 0
            self.doorstate = data["Door state"]
            self.timestamp = data["Time Stamp"]
            self.mainframe.DisplayStatus(str(self.doorstate))


    def publish(self, topic, message):
        """
        Publishes a message on the broker
        :param topic: the topic to publish to
        :param message: the message to publish
        :return: no return value
        """
        self.client.publish(topic, bytes(message, 'utf-8'))
