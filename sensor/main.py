from magnetometer import Magnetometer
# The following line  had 'magnetometer' instead  of 'calibration'
from calibration import Lock
from networking import WiFi
from networking import MQTTManager
import utime
from calibration import DataLogger
from utility import Status
from ujson import dumps

wifi_conn = WiFi()  #establishes a wifi connection
magnetometer = Magnetometer()
mqttmanager = MQTTManager()
lock = Lock()
status = Status()

# Let the door status be open (3)
currentStatus = status.getStatusCode("UNCALIBRATED")
mqttmanager.publish("esys/dadada/status",currentStatus)

while currentStatus == status.getStatusCode("UNCALIBRATED"):
    # do nothing until the calibration has been completed (status == 4)
    mqttmanager.publish("esys/dadada/status","Waiting for calibration")
    if not wifi_conn.station.active():
        wifi_conn.connect()

    if mqttmanager.status==1:
        lock.calibrate_locked()
        mqttmanager.publish("esys/dadada/status",status.getStatusCode("CALIBRATING"))
        print("calib locked")
    elif mqttmanager.status==2:
        lock.calibrate_closed()
        mqttmanager.publish("esys/dadada/status", status.getStatusCode("CALIBRATING"))
        print("calib closed")
    elif mqttmanager.status==3:
        lock.calibrate_open()
        mqttmanager.publish("esys/dadada/status", status.getStatusCode("CALIBRATING"))
        print("calib open")
        currentStatus = "5"
    utime.sleep_ms(300)

    mqttmanager.client.check_msg()
    

while(True):
    #if mqttmanager.publish("esys/dadada/wificheck",lock.logger.get_json()):
    #    wifi_conn.connect()
    if not wifi_conn.station.active():
        wifi_conn.connect()
    
    mqttmanager.publish("esys/dadada/status","Calibratedaaaaaaaaaaaaaaaaaaa")
    # update MQTT broker when door changes state
    nextState = lock.get_status()
    print("Current: " + str(currentStatus))
    if currentStatus != nextState:
        currentStatus = nextState    # save the current door state
        mqttmanager.publish("esys/dadada/status", currentStatus)   #update mqtt
        print("Status changed, now " + str(currentStatus))

    mqttmanager.client.check_msg()
    utime.sleep_ms(300)