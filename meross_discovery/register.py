# -*- coding: utf-8 -*-

###################################################################################################
# Registers new discovered devices with mosquitto addon and home assistant meross component 
# - Mosquitto access control list
# - Mosquitto users
# - Device details
# 


import subprocess
import requests
import base64
import subprocess
import time
import os
import sys
import pprint
from meross_discovery.registration.ha_component import devices
from meross_discovery.registration.mqtt_broker import acl, logins
from meross_discovery.registration.meross import device_api
from .configuration import Config

def go(opts):

    try:
        dev0 = device_api.get_device_data()

        config=Config(opts.config)

        device = dev0["payload"]["all"]["system"]
        uuid = device["hardware"]["uuid"]
        mac = device["firmware"]["wifiMac"]
        fmwareVersion = device["firmware"]["version"]
        hdwareVersion = device["hardware"]["version"]
        subType = device["hardware"]["subType"]
        deviceType = device["hardware"]["type"]

        devices.add_device(
            uuid=uuid,
            devName=opts.name,
            mac=mac,
            deviceType=deviceType,
            domain=config.mqtt_server(),
            fmwareVersion=fmwareVersion,
            hdwareVersion=hdwareVersion,
            subType=subType,
            devices_path=config.devices_path()
        )

        acl.add_device(device_uuid=uuid, mac=mac, acl_path=config.acl_path(), user_id=config.user_id(), app_uuid=config.app_uuid())

        logins.add_device(mac=mac, logins_path=config.logins_path(), auth_key=config.auth_key(), user_id=config.user_id())

        device_api.set_server_details(mqttServer=config.mqtt_server(), port=config.mqtt_port(), key=config.auth_key(), user_id=config.user_id())
        
        device_api.set_wifi_details(password=config.ssid_password(), ssid=config.ssid())

        print(f"Added {opts.name} ({deviceType})")

    except subprocess.CalledProcessError:
        pass
