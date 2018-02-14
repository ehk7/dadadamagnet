import paho.mqtt.client as mqtt

class MQTTManager:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("192.168.0.10", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("esys/time")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def publish(self, topic, message):
        self.client.publish(topic, message)


