from magnetometer import Magnetometer
# The following line  had 'magnetometer' instead  of 'calibration'
from calibration import Lock
from networking import WiFi
from networking import MQTTManager
import utime
from utility import Status


#connect to wifi
wifi_conn = WiFi()


#init
mqttmanager = MQTTManager()
lock = Lock()
status = Status()

#at init send status uncalibrated
currentStatus = status.getStatusCode("UNCALIBRATED") #1

while currentStatus == status.getStatusCode("UNCALIBRATED"): #1
    # do nothing until the calibration has been completed (status == 4)
    #mqttmanager.publish("esys/dadada/status", currentStatus)
    if not wifi_conn.station.active():
        wifi_conn.connect()

    if mqttmanager.status==status.getStatusCode("LOCKED"): #calibrate for locked state
        lock.calibrate_locked()
        mqttmanager.publish("esys/dadada/status",status.getStatusCode("LOCKED")) #2
        mqttmanager.status=0
        print("calib locked")

    elif mqttmanager.status==status.getStatusCode("CLOSED"): #calibrate closed&unlocked state
        lock.calibrate_closed()
        mqttmanager.publish("esys/dadada/status", status.getStatusCode("CLOSED")) #2
        mqttmanager.status = 0
        print("calib closed")

    elif mqttmanager.status==status.getStatusCode("OPEN"): #open state
        lock.calibrate_open()
        mqttmanager.publish("esys/dadada/status", status.getStatusCode("OPEN")) #2
        mqttmanager.status = 0
        print("calib open")

        currentStatus = status.getStatusCode("OPEN") #OPEN
    utime.sleep_ms(300)

    mqttmanager.client.check_msg()

#mqttmanager.publish("esys/dadada/status","Calibrated")
print("entering main loop")

while(True):
    #if mqttmanager.publish("esys/dadada/wificheck",lock.logger.get_json()):
    #    wifi_conn.connect()
    if not wifi_conn.station.active():
        wifi_conn.connect()

    # update MQTT broker when door changes state
    nextState = lock.get_status()
    mqttmanager.publish("esys/dadada/status2", currentStatus)

    if currentStatus != nextState:
        currentStatus = nextState    # save the current door state
        mqttmanager.publish("esys/dadada/status", currentStatus)   #update mqtt

    mqttmanager.client.check_msg()
    utime.sleep_ms(300)