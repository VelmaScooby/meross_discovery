# -*- coding: utf-8 -*-


from meross_discovery.registration.ha_component import devices
from meross_discovery.registration.mqtt_broker import acl, logins

def go(opts):
    device=opts.name

    devices_details=devices.get_details(device) 
    devices.delete_device(device)

    for device_details in devices_details:
        acl.delete_device(mac=device_details["mac"],uuid=device_details["uuid"])
        logins.delete_device(mac=device_details["mac"])

    