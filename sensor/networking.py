import network
from umqtt.simple import MQTTClient
import machine
import ubinascii
import utime
from ujson import dumps


class MQTTManager:
    """Manages communication to/from the MQTT broker"""
    def __init__(self, client_id="", broker = "192.168.0.10"):
        """Creates an MQTTClient with broker details, subscribes to initial control topic (esys/dadada/userstatus)
         and clock, and adds a callback to handle messages"""

        #create a client ID if none provided
        if client_id == "":
            self.client_id = ubinascii.hexlify(machine.unique_id())
        else:
            self.client_id = client_id

        #set up default broker if one is not provided and create MQTTClient a member variable of the class
        self.broker = broker
        self.client = MQTTClient(self.client_id, self.broker)

        #timestamp stored as a member var
        self.timestamp = 0
        while True:
            try:
                self.client.connect()
                break
            except OSError as e:
                utime.sleep_ms(200)

        #set up callback to handle message published in subscribed topics
        self.client.set_callback(self.on_message)

        self.client.subscribe("esys/time")
        self.client.subscribe("esys/dadada/userstatus")

        self.status = 0

    def publish(self, topic, doorState):
        """encodes door state in JSON and publishes to the broker"""
        #TODO: implement encryption here
        messageToSend = {
            "Door state" : doorState,
            "Time Stamp" : self.timestamp
        }

        try:
            self.client.publish(topic, bytes(dumps(messageToSend), 'utf-8'), 1)
        except OSError as e:
            #error occured, return bad status
            return 1
        #return succesful status
        return 0


    def on_message(self, topicBytes, msgBytes):
        print(topicBytes)
        """callback to get calibration instructions from user"""

        #decode binary to utf-8 strings
        topic = topicBytes.decode("utf-8")
        message = msgBytes.decode("utf-8")

        if topic == "esys/time":
            #update timestamp
            self.update_timestamp(message)

        if topic == "esys/dadada/userstatus":
            #convert to integer status code
            self.status = int(message)



    def update_timestamp(self, message):
        """callback to update timestamp, converting the time string into a timestamp"""
        #split into date and time
        date, time = message.split("T")
        dateArr = date.split("-")
        timeArr = time.split(":")

        #mktime handles conversion to a timestamp
        self.timestamp=utime.mktime((int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(timeArr[0]), int(timeArr[1]), int(timeArr[2][:2]), 0, 0))

class WiFi:
    """CLass to manage the WiFI connection"""
    def __init__(self, ssid = "EEERover", password = "exhibition", is_AP = False):
        #stores ssid and password so reconnection is possible
        #easily support connecting to other networks, defaults to EERover
        self.set_ssid(ssid)
        self.set_password(password)

        #also supports functioning as an access point if necessary
        #(not used in this project)
        self.station = network.WLAN(network.STA_IF)
        self.AP = network.WLAN(network.AP_IF)

        #defaults to station mode
        if is_AP==True:
            self.start_AP()
        else:
            self.connect()

    def connect(self):
        #disable AP and activate station mode
        self.AP.active(False)
        self.station.active(True)

        #use stored username and password
        self.station.connect(self.ssid, self.password)

        #keep trying until connection established
        while not self.station.isconnected():
            pass

    def start_AP(self):
        #start access point with set ssid and password
        self.AP.active(True)
        self.AP.connect(self.ssid, self.password)

    def set_ssid(self, ssid):
        self.ssid = ssid

    def set_password(self, password):
        self.password = password

