###################################################################################################
# Meross devices receive commands and publish their status to a certain topics
# This components builds topics and other parameters required for meross devices
# to function.
# In other words this is meross-mqtt protocol implemetaion
# 
# 
# 
#
# 
# 

import uuid as UUID
import logging
import pprint 
from hashlib import md5

def build_device_request_topic(device_uuid: str) -> str:
    """
    Builds the MQTT topic where commands should be send to specific devices
    :param device_uuid:
    :return:
    """
    return f"/appliance/{device_uuid}/subscribe"


def build_client_response_topic(user_id: str, app_id: str) -> str:
    """
    Builds the MQTT topic where the device sends back ACKs to commands
    :param app_id:
    :param user_id:
    :param device_uuid:
    :return:
    """
    return f"/app/{user_id}-{app_id}/subscribe"


def build_client_user_topic(user_id: str):
    """
    Builds the topic name where user push notification are received
    :param user_id:
    :return:
    """
    return f"/app/{user_id}/subscribe"

def generate_client_and_app_id(app_uuid:str):
    """
    Generates a new app-id.
    :return:
    """
    # TODO: Talk to the Meross engineer and check if the APPID should be the same or if we
    #  need to use a convention to discriminate MerossIot python clients.
    md5_hash = md5()
    rnd_uuid = app_uuid
    md5_hash.update(f"API{rnd_uuid}".encode("utf8"))
    app_id = md5_hash.hexdigest()
    client_id = 'app:%s' % md5_hash.hexdigest()
    return app_id, client_id


def generate_mqtt_password(mac: str, key: str, user_id: str):
    """
    Generates the MQTT password that the APP uses to connect to the mqtt server.
    :param user_id:
    :param key:
    :return:
    """
    md5_hash = md5()
    clearpwd = f"{mac}{key}"
    md5_hash.update(clearpwd.encode("utf8"))
    password = f"{user_id}_{md5_hash.hexdigest()}"
    return password
