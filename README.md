# meross_discovery
Simple command line interface for local operation of Meross IoT kit

Incorporates iwlist.py from https://github.com/iancoleman/python-iwlist as I couldn't figure out how to include it without running into problems when trying to package this stuff up so it was suitable for "pip install".

You must be in a sudo group to run all of the wifi commands to connect to Meross device.

To initialise local config files:

For the user:

Give the name of the mqtt server, port number and path to certificate file if required and your local wifi network name and password:

`./meross init --server SERVER --port PORT --ca-cert /path/to/ca.crt --ssid SSID --password PASSWORD --config "~/.config/meross_discovery/config.json"

The configuration is stored in .config/meross_discovery/config.json relative to the home directory and has a "chmod 600" performed on it.

Once that's done you don't need to think about those options, you can change them with a `config` sub-command though.

./meross register --config "~/.config/meross_discovery/config.json

register the device woth mqtt server and meross homeassistant integration

To add a device:

`./meross setup name`

Will bring up the wifi device and scan for an AP name starting with "Meross_"

We then associate with the Meross_* network

Next we configure the wifi network with an appropriate IP address and route and gather some device data (which we'll store later). Then it's a case of giving the device details of the MQTT server to use and the ssid and password for our normal wifi network.

Finally the device data is stored in the named user's config file using the name given in the setup command.
# meross_discovery
# meross_discovery
# meross_discovery
# meross_discovery
