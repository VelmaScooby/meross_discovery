###################################################################################################
# Since meross devices connect to a mqtt server with a password derived from user_id, key and 
# device name I needed a way to control authentication on mosquitto server.
# I didn't want to add login details for each user to mosquitto addon configuration for security reasons
# To work around this I changed authentication provider of the mosquitto server to look for users in 
# logins.json in addition to file derived from the addon configuration.
# 
# The better way would be to add a system user for each meross device to a homeassistant users registry,
# but I didn't want to spend more time on this issue
# 
# logins.json format mimics logins.json derived from the addon configuration
# 
# This component adds or removes device credetials to logins.json
#

import json
import os
import sys
import time
from hashlib import md5
from pathlib import Path
from json.decoder import JSONDecodeError
from typing import Optional, List, TypeVar, Iterable, Callable, Awaitable, Tuple
from .meross_mqtt import generate_mqtt_password

def add_device(mac:str, logins_path: str, auth_key: str, user_id: str) -> None:

  logins=load(logins_path)

  if not "logins" in logins:
    logins["logins"]=[]

  _delete_device(mac,logins)

  logins["logins"].append(generateLogin(mac, auth_key, user_id))
  
  save(logins, logins_path)

def delete_device(mac: str, logins_path: str):
  logins=load(logins_path)
 
  if not "logins" in logins:
    logins["logins"]=[]
  
  _delete_device(mac=mac, logins=logins)
  
  save(logins, logins_path)

def _delete_device(mac: str, logins: {}):
  
  if not logins["logins"]:
    return
  del_login=[l for l in logins["logins"] if l["username"] == mac]
  
  [logins["logins"].remove(l) for l in del_login]

def generateLogin(mac:str, key: str, user_id: str):
  login = {}
  login["username"]=mac
  login["password"]=generate_mqtt_password(mac,key,user_id)
  return login
  
def load(path):
  logins = dict()

  fullPath = _expandPath(path)
  logins_str=fullPath.read_text()    
  try:
    logins=json.loads(logins_str)
  except JSONDecodeError:
    pass

  return logins

def save(logins, path):
  fullPath = _expandPath(path)
  fullPath.write_text(json.dumps(logins,indent=2))

def _expandPath(path) -> Path:
  fullPath = Path.expanduser(Path(path))
  if not fullPath.exists():
    fullPath.touch(mode=0o664,exist_ok=True)

  return fullPath

