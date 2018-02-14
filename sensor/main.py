from magnetometer import Magnetometer
from magnetometer import Lock
from networking import WiFi
from networking import MQTTManager
import time
from calibration import DataLogger

wifi_conn = WiFi()  #establishes a wifi connection
magnetometer = Magnetometer()
mqttmanager = MQTTManager()
lock = Lock()

while(True):
    if mqttmanager.publish("SensorData",lock.logger.get_json()):
        wifi_conn.connect()

    if mqttmanager.status==1:
        lock.calibrate_locked()
        mqttmanager.publish("esys/dadada/status","2")
    elif mqttmanager.status==2:
        lock.calibrate_closed()
        mqttmanager.publish("esys/dadada/status", "2")
    elif mqttmanager.status==3:
        lock.calibrate_open()
        mqttmanager.publish("esys/dadada/status", "2")

    time.sleep_ms(5000)