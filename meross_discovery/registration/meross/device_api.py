# -*- coding: utf-8 -*-

###################################################################################################
# Communicates with meross devices
# Should run on a machine connected to a device wifi access point
# Requests device details and sends to device information regarding mqtt server and local wifi
# 
# 
# 
# 
#
# 
# 

import subprocess
import requests
import base64
import subprocess
import time
import os
import sys
import pprint

URL = "http://10.10.10.1"
HEADERS = dict(
    {
        "from": "",
        "messageId": "",
        "method": "GET",
        "namespace": "Appliance.System.All",
        "payloadVersion": "",
        "sign": "",
        "timestamp": "",
    }
)

def send(url, data):
    r = requests.post(url, json=data)
    if r.status_code != 200:
        print("status: ", r.status_code)
        sys.exit("error sending request to device: {}".format(url))
    return r.json()


def get_device_data(url=URL):
    headers = HEADERS.copy()
    payload = dict()
    data = dict({"header": headers, "payload": payload})
    return send(url + "/config/", data)


def set_server_details(mqttServer:str, port:str, key:str, user_id:str, url:str=URL):
    header = HEADERS.copy()
    header["method"] = "SET"
    header["namespace"] = "Appliance.Config.Key"
    header["payloadVersion"] = 1
    header["timestamp"] = 0

    payload = dict(
        {
            "key": {
                "gateway": {
                    "host": mqttServer,
                    "port": port,
                    "secondHost": mqttServer,
                    "secondPort": port,
                },
                "key": key,
                "userId": user_id,
            }
        }
    )

    data = dict({"header": header, "payload": payload})
    return send(URL + "/config/", data)


def set_wifi_details(ssid:str, password:str, url:str=URL):
    header = HEADERS.copy()
    header["method"] = "SET"
    header["namespace"] = "Appliance.Config.Wifi"
    header["payloadVersion"] = 0
    header["timestamp"] = 0
    payload = dict(
        {
            "wifi": {
                "bssid": "",
                "channel": 1,
                "cipher": 3,
                "encryption": 6,
                "password": password,
                "ssid": ssid,
            }
        }
    )
    data = dict({"header": header, "payload": payload})
    return send(URL + "/config/", data)
