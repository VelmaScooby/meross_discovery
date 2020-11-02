import yaml
import uuid
import base64
from pathlib import Path
from getpass import getpass


APP_UUID_KEY="app_uuid"
USER_ID_KEY="user_id"
AUTH_KEY="auth_key"
HASSIO_KEY="hassio_installation_folder"
DATA_FOLDER_KEY="data_folder"
MOSQUITTO_KEY="mosquitto"
SHARE_FOLDER_KEY="share_folder"
HA_COMPONENT_KEY="ha_component"
SERVER_KEY="server"
PORT_KEY="port"
SSID_KEY="ssid"
SSID_PASSWORD_KEY="password"
MEROSS_KEY="meross"

class Config:
  def __init__(self, config_path:str):
    self._load(config_path)

  def app_uuid(self):

    if MEROSS_KEY not in self.data:
      self.data[MEROSS_KEY]={APP_UUID_KEY:uuid.uuid4().hex}
      self.save()
    if APP_UUID_KEY not in self.data[MEROSS_KEY]:
      self.data[MEROSS_KEY][APP_UUID_KEY]=uuid.uuid4().hex
      self.save()

    return self.data[MEROSS_KEY][APP_UUID_KEY]

  def user_id(self):
    #TODO: will be provided by meross html server mock
    if MEROSS_KEY not in self.data:
      self.data[MEROSS_KEY]={USER_ID_KEY:"490834"}
      self.save()
    if USER_ID_KEY not in self.data[MEROSS_KEY]:
      self.data[MEROSS_KEY][USER_ID_KEY] = "490834"
      self.save()
      
    return self.data[MEROSS_KEY][USER_ID_KEY]

  def auth_key(self):
    #TODO: will be provided by meross html server mock
    if MEROSS_KEY not in self.data:
      self.data[MEROSS_KEY]={AUTH_KEY:"da005b0da2988e9e7f8c5b21177f318e"}
      self.save()
    if AUTH_KEY not in self.data[MEROSS_KEY]:
      self.data[MEROSS_KEY][AUTH_KEY]="da005b0da2988e9e7f8c5b21177f318e"
      self.save()
      
    return self.data[MEROSS_KEY][AUTH_KEY]
  
  def acl_path(self):
   #TODO: read from mosquitto config or add to mosquitto config
   return f"{self.data[HASSIO_KEY]}/{self.data[MOSQUITTO_KEY][SHARE_FOLDER_KEY]}/accesscontrollist"

  def logins_path(self):
    return f"{self.data[HASSIO_KEY]}/{self.data[MOSQUITTO_KEY][DATA_FOLDER_KEY]}/logins.json"

  def devices_path(self):
    return f"{self.data[HASSIO_KEY]}/{self.data[MEROSS_KEY][HA_COMPONENT_KEY]}/devices.json"

  def mqtt_server(self):
    return self.data[MOSQUITTO_KEY][SERVER_KEY]

  def mqtt_port(self):
    return self.data[MOSQUITTO_KEY][PORT_KEY]

  def ssid(self):
    if self._ssid == None:
      self._init_ssid_details()
    return self._ssid

  def ssid_password(self):
    if self._password == None:
      self._init_ssid_details()
    return self._password

  def save(self):
    with self._path.open(mode='w') as stream:
      yaml.safe_dump(data=self.data, stream=stream, indent=2)

  def _load(self, path:str):
    file=self._expandPath(path)
    with file.open(mode='r') as stream:
      self.data = yaml.full_load(stream)
      self._password=None
      self._ssid=None
      self._path=file

  def _expandPath(self, path:str):
    fullPath = Path.expanduser(Path(path))
    if not fullPath.exists():
      fullPath.touch(mode=0o664,exist_ok=True)

    return fullPath

  def _init_ssid_details(self):
    self._ssid=(self.data[MEROSS_KEY][SSID_KEY] 
        if MEROSS_KEY in self.data and SSID_KEY in self.data[MEROSS_KEY] 
        else self._mangle(input(f'Provide local network name: ')))

    self._password=(self.data[MEROSS_KEY][SSID_PASSWORD_KEY] 
        if MEROSS_KEY in self.data and SSID_PASSWORD_KEY in self.data[MEROSS_KEY] 
        else self._mangle(getpass(f'Provide local network password: ')))

    self.save()

  def _mangle(self, s):
    return str(base64.b64encode(s.encode("utf-8")), "utf-8")