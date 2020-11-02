###################################################################################################
# Manages entries in access control list file of the mosquitto serve
# Each meross device must have access to the following topics:
#   topic /appliance/<device uuid>/subscribe
#   topic /appliance/<device uuid>/publish
#   topic /app/<user_id>-<app_id>/subscribe
# User associated with the home assistant component must have access to this topic:
#   topic /appliance/<device uuid>/subscribe  
# 
# This component adds access control entries for meross devices when new devices discovered 
# and removes entries

import json
import os
import sys
import time
import pprint
from pathlib import Path
from json.decoder import JSONDecodeError
from typing import Optional, List, TypeVar, Iterable, Callable, Awaitable, Tuple
from .meross_mqtt import build_device_request_topic, build_client_response_topic, generate_client_and_app_id

def add_device(device_uuid:str, mac:str, acl_path: str, user_id: str, app_uuid: str):
  lines=_load(acl_path)
  lines=_delete_device(device_uuid=device_uuid, mac=mac, lines=lines)
  lines.extend(_deviceAclLines(user_id, device_uuid, mac, app_uuid))
  _save(lines,acl_path)

def delete_device(device_uuid:str, mac:str, path: str):
  lines=_load(path)
  lines=_delete_device(device_uuid,mac,lines)
  _save(lines, path)

def _delete_device(device_uuid:str, mac:str, lines: []):
  dev_lines=[]
  for l in range(len(lines)):
    if f"topic /appliance/{device_uuid}/subscribe" in lines[l]:
      i=l-1
      while lines[i].strip() == '' and i>=0:
        i -= 1
      if "user" in lines[i]:
        dev_lines.append(i)
      dev_lines.append(l)
      
          
    if f"user {mac}" in lines[l]:
      dev_lines.append(l)
      i=l+1
      while i < len(lines) and not "user" in lines[i] :
        if lines[i].strip():
          dev_lines.append(i)
        i+=1

  [lines[l] for l in range(len(lines)) if l not in dev_lines]
  
  return [lines[l] for l in range(len(lines)) if l not in dev_lines]

def _deviceAclLines(user_id: str, device_uuid:str, mac:str, app_uuid:str):

  device_request_topic=build_device_request_topic(device_uuid=device_uuid)
  app_id,_=generate_client_and_app_id(app_uuid)
  client_response_topic=build_client_response_topic(user_id=user_id,app_id=app_id)
  
  return [f"user {user_id}\n",
          f"topic {device_request_topic}\n",
          f"user {mac}\n",
          f"topic {device_request_topic}\n",
          f"topic /appliance/{device_uuid}/publish\n",
          f"topic {client_response_topic}\n"]
  
def _load(path):
  lines = []
  fullPath = _expandPath(path)
  
  with fullPath.open(mode='r') as file:
    lines = file.readlines()

  return [x for x in lines]

def _save(lines:list, path:str):
  fullPath = _expandPath(path)

  with fullPath.open(mode='w') as file:
    file.writelines(lines)

def _expandPath(path) -> Path:
  fullPath = Path.expanduser(Path(path))
  if not fullPath.exists():
    fullPath.touch(mode=0o664,exist_ok=True)

  return fullPath
