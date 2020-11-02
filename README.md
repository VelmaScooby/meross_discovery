# meross_discovery
Simple command line interface to discover and register meross devices with local mosquitto server and meross_offline ha custom component

You must be in a sudo group to run all of the wifi commands to connect to Meross device.

This utility scans local wifi networks in search for access points what start with Meross*.
Connects to each access point and receives details about the device: firmware version, mac, model etc'
    -adds relevant entries to mosquitto access controll list
    -adds a user on mosquitto for each device
    -adds device info to a meross component on home assistant
    -configures Meross devices to connect to local network and work with local mosquitto server
    -generates config.yaml for reuse


TODO:
add usage instructions to read.me
generate config.yaml locally and then copy it to the meross_offline component
create html server to mock meross html
contact meross_cloud creator to allow configuration for mqtt server and meross html server 