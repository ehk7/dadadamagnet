from magnetometer import Magnetometer
from networking import WiFi
from networking import MQTTManager
import time
from calibration import DataLogger

wifi_conn = WiFi()  #establishes a wifi connection
magnetometer = Magnetometer()
mqttmanager = MQTTManager()
logger = DataLogger(magnetometer)

while(True):
    logger.measure()
    mqttmanager.publish("SensorData",logger.get_json())
    time.sleep_ms(5000)