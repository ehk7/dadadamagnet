import network
from umqtt.simple import MQTTClient
import machine


class MQTTManager:
    """Manages communication to/from the MQTT broker"""
    def __init__(self, client_id=""):
        self.topic = "esys/dadada/"
        if client_id == "":
            self.client_id = machine.unique_id()
        else:
            self.client_id = client_id
        self.broker = broker
        self.client = MQTTClient(self.client_id, self.broker)
        self.timestamp = ""
        self.client.set_callback(self.on_message())
        self.client.connect()
        self.client.subscribe("esys/time")
        self.client.subscribe("esys/dadada/status")

    def publish(self, topic, message):
        """publish message to the broker with topic"""
        #TODO: implement encryption here
        self.client.publish(topic, message)

    def on_message(self, topic, message):
        """callback to get calibration instructions from user"""
        if topic == "esys/time":
            self.update_timestamp(message)
        elif topic == "esys/dadada/status":


    def update_timestamp(self, message):
        """callback to update timestamp"""
        self.timestamp=message

class WiFi:
    """CLass to manage the WiFI connection"""
    def __init__(self, ssid = "EEERover", password = "exhibition", is_AP = False):
        self.set_ssid(ssid)
        self.set_password(password)

        self.station = network.WLAN(network.STA_IF)
        self.AP = network.WLAN(network.AP_IF)

        if is_AP==True:
            self.start_AP()
        else:
            self.connect()

    def connect(self):
        self.AP.active(False)
        self.station.active(True)
        self.station.connect(self.ssid, self.password)

        while not self.station.isconnected():
            pass

    def start_AP(self):
        self.AP.active(True)
        self.AP.connect(self.ssid, self.password)

    def set_ssid(self, ssid):
        self.ssid = ssid

    def set_password(self, password):
        self.password = password


class Encryption:
    pass
