import network
from umqtt.simple import MQTTClient
import machine
import ubinascii
import utime
from utility import Status
from ujson import dumps


class MQTTManager:
    """Manages communication to/from the MQTT broker"""
    def __init__(self, client_id="", broker = "192.168.0.10"):
        self.topic = "esys/dadada/"
        if client_id == "":
            self.client_id = ubinascii.hexlify(machine.unique_id())
        else:
            self.client_id = client_id
        self.broker = broker
        self.client = MQTTClient(self.client_id, self.broker)
        self.timestamp = 0
        
        self.client.connect()
        self.client.set_callback(self.on_message)
        self.client.subscribe("esys/time")
        self.client.subscribe("esys/dadada/userstatus")
        self.status = 0

    def publish(self, topic, doorState):
        """publish message to the broker with topic"""
        #TODO: implement encryption here
        messageToSend = {
            "Door state" : doorState,
            "Time Stamp" : self.timestamp
        }

        try:
            self.client.publish(topic, bytes(dumps(messageToSend), 'utf-8'), 1)
        except OSError as e:
            return 1

        return 0


    def on_message(self, topBytes, mesBytes):
        print(topBytes)
        """callback to get calibration instructions from user"""
        topic = topBytes.decode("utf-8")
        message = mesBytes.decode("utf-8")
        if topic == "esys/time":
            print("time should be updated")
            self.update_timestamp(message)
        if topic == "esys/dadada/userstatus":
            self.status = int(message)
            print("userdata")



    def update_timestamp(self, message):
        """callback to update timestamp"""
        dateTimeArr = message.split("T")
        date, time = dateTimeArr
        dateArr = date.split("-")
        timeArr = time.split(":")
        self.timestamp=utime.mktime((int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(timeArr[0]), int(timeArr[1]), int(timeArr[2][:2]), 0, 0))

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
