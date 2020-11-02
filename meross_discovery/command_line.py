# -*- coding: utf-8 -*-

import argcomplete
import argparse
import base64
import sys
import os
from getpass import getpass

from meross_discovery.version import VERSION
from meross_discovery import (delete, register)

REGISTER_SUBCMD="register"
DELETE_SUBCMD="delete"
def arguments(*args):
    # Parser to store arguments
    parser = argparse.ArgumentParser(description="meross ({}) - A tool for "
                                                 "local use of Meross IoT "
                                                 "kit".format(VERSION))

    # Subcommands
    subparser = parser.add_subparsers(dest="subcommand")
    subcommands = dict()

    subcommands[REGISTER_SUBCMD] = register
    register_parser = subparser.add_parser(REGISTER_SUBCMD, description="Register the device with meross homeassistant component and mqtt broker")
    register_parser.add_argument('--config', help="Path to a config file")
    register_parser.add_argument('--ssid', help="local wifi network name")
    register_parser.add_argument('--password', help="local wifi network password")
    register_parser.add_argument('name', help="Local name for Meross device")

    argcomplete.autocomplete(parser, always_complete_options=False)

    subcommands[DELETE_SUBCMD] = delete
    delete_parser = subparser.add_parser(DELETE_SUBCMD, description="Delete device from mqtt configutaion")
    delete_parser.add_argument('name', help="Name of a device to be deleted")
     
    return (parser.parse_args(*args), subcommands)