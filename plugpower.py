#!/usr/bin/python
#
# Power Probe - Wattage of smartplugs - JSON Output

import pytuya
from time import sleep
import datetime

# Device Info - EDIT THIS
DEVICEID="123"
DEVICEIP="123"
LOCALKEY="123"

# MQTT server - EDIT THIS
MQTTSERVER="www.example.com"
MQTTUSER="user"
MQTTPASSWORD="password"
MQTTTOPIC="sensor/tuyaswitch/plug1/"

# how my times to try to probe plug before giving up
RETRY=5

def deviceInfo( deviceid, ip ,localkey):
    watchdog = 0
    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, localkey)
            data = d.status()
            if(d):
                print('Dictionary %r' % data)
                print('Switch On: %r' % data['dps']['1'])
                if '5' in data['dps'].keys():
                    #print('Power (W): %f' % (float(data['dps']['5'])/10.0))
                    #print('Current (mA): %f' % float(data['dps']['4']))
                    #print('Voltage (V): %f' % (float(data['dps']['6'])/10.0))
                    mqttc = mqtt.Client(MQTTUSER)
                    mqttc.username_pw_set(MQTTUSER, MQTTPASSWORD)
                    mqttc.connect(MQTTSERVER, 1883)
                    mqttc.publish(MQTTTOPIC+"watt", str(float(data['dps']['5'])/10.0),retain=False)
                    mqttc.publish(MQTTTOPIC+"current", data['dps']['4'],retain=False)
                    mqttc.publish(MQTTTOPIC+"voltage", str(float(data['dps']['6'])/10.0),retain=False)
                    mqttc.loop(2)


                    return(float(data['dps']['5'])/10.0)
                else:
                    return(0.0)
            else:
                return(0.0)
            break
        except KeyboardInterrupt:
            pass
        except:
            watchdog+=1
            if(watchdog>RETRY):
                print("ERROR: No response from plug %s [%s]." % (deviceid,ip))
                return(0.0)
            sleep(2)

print("Polling Device %s at %s" % (DEVICEID,DEVICEIP))

devicepower = deviceInfo(DEVICEID,DEVICEIP,LOCALKEY)

