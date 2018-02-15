"""
The main module that is executed on boot by the ESP8266
The module contains no class definition and consists of two main loops, one for setting up the device and recording
magnetometer measurements for each of the device states (locked, closed/unlocked, open), and the other for continuously
monitoring the state and acting on any changes.
"""
# The following line  had 'magnetometer' instead  of 'calibration'
from calibration import Lock
from networking import WiFi
from networking import MQTTManager
import utime
from alarm import Alarm
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
    if not wifi_conn.station.active():
        wifi_conn.connect()

    if mqttmanager.status==status.getStatusCode("LOCKED"): #calibrate for locked state
        lock.calibrate_locked()
        mqttmanager.publish("esys/dadada/status",status.getStatusCode("LOCKED")) #2
        mqttmanager.status=0

    elif mqttmanager.status==status.getStatusCode("CLOSED"): #calibrate closed&unlocked state
        lock.calibrate_closed()
        mqttmanager.publish("esys/dadada/status", status.getStatusCode("CLOSED")) #2
        mqttmanager.status = 0

    elif mqttmanager.status==status.getStatusCode("OPEN"): #open state
        lock.calibrate_open()
        mqttmanager.publish("esys/dadada/status", status.getStatusCode("OPEN")) #2
        mqttmanager.status = 0

        currentStatus = status.getStatusCode("OPEN") #OPEN
    utime.sleep_ms(300)

    mqttmanager.client.check_msg()

alarm = Alarm()
alarm_on = False

while(True):
    if mqttmanager.alarm_status==1 and (currentStatus==status.getStatusCode("OPEN") or currentStatus==status.getStatusCode("CLOSED")):
        alarm.beep()

    if not wifi_conn.station.active():
        wifi_conn.connect()

    # update MQTT broker when door changes state
    nextState = lock.get_status()

    if currentStatus != nextState:
        currentStatus = nextState    # save the current door state
        mqttmanager.publish("esys/dadada/status", currentStatus)   #update mqtt

    mqttmanager.client.check_msg()
    utime.sleep_ms(300)