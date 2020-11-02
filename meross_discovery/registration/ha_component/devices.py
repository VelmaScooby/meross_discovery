###################################################################################################
# Meross http server stores devices basic information. Since I wanted to have local mqtt server
# this components generates a file with connected meross devices. Home assistant meross component 
# uses this information to facilitate homeassistant and meross communication.
# 
# Edit devName in devices_list.json to change device name
# 
# This component adds device details to devices_list.json
#

import json
import os
import sys
import time
import pprint
from pathlib import Path
from json.decoder import JSONDecodeError
from typing import Optional, List, TypeVar, Iterable, Callable, Awaitable, Tuple

def add_device(uuid: str,
  devName: str,
  mac: str,
  deviceType: str,
  domain: str,
  fmwareVersion: str,
  hdwareVersion: str,
  subType: str,
  devices_path: str,
  region: str="us",
  skillNumber: str="",
  reservedDomain: Optional[str] = None) -> None:

  devices=load(devices_path)
  
  for d in devices:
    if d["uuid"] == uuid:
      devices.remove(d)
      break

  device = generateDevice(devName, mac, deviceType, domain, fmwareVersion, hdwareVersion, region, reservedDomain, subType, uuid)
  devices.append(device)
  save(devices, devices_path)

def get_details(name: str, devices_path: str):
  all_devices=load(devices_path)
  return [device for device in all_devices if device["devName"]==name]

def delete_device(name: str, devices_path: str):
  devices=load(devices_path)
  dev_delete= [device for device in devices if device["devName"]==name]

  save([devices.remove(device) for device in dev_delete],devices_path)

def generateDevice(devName, mac, deviceType, domain, fmwareVersion, hdwareVersion, region, reservedDomain, subType, uuid) -> dict:
  device = {}
  device["bindTime"] = int(time.time())
  device["channels"] = [{}]
  device["devIconId"] = ""
  device["devName"] = devName
  device["deviceType"] = deviceType
  device["domain"] = domain
  device["fmwareVersion"] = fmwareVersion
  device["hdwareVersion"] = hdwareVersion
  device["iconType"] = 1
  device["onlineStatus"] = 1
  device["region"] = region
  device["reservedDomain"] = reservedDomain if reservedDomain == None else domain
  device["skillNumber"] = ""
  device["subType"] = subType
  device["userDevIcon"] = ""
  device["uuid"] = uuid
  device["mac"] = mac
  return device
  
def load(path):
  devices = []

  fullPath = _expandPath(path)
  devices_str=fullPath.read_text()    
  try:
    devices.extend(json.loads(devices_str))
  except JSONDecodeError:
    pass

  return devices

def save(devices, path):
  fullPath = _expandPath(path)
  fullPath.write_text(json.dumps(devices,indent=2))

def _expandPath(path) -> Path:
  fullPath = Path.expanduser(Path(path))
  if not fullPath.exists():
    fullPath.touch(mode=0o664,exist_ok=True)

  return fullPath
