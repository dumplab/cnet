""" A network infrastructure Configuration Item (CI) which delivers an IT Service
 
A network item can be a Switch, Router or other Managed Infrastructure Component
"""

__author__    = "dumplab"
__copyright__ = "2016 dumplab"
__license__   = "MIT"
__version__   = "1.1"
__status__    = "Production"

import json

class cNetDevice(object):
	"""Represents a network device"""

	def __init__(self,name="",vendor="",deviceType="",ipv4="",ipv6="",serial="",building="",floor="",room="",rack="",isMonitored=0):
		"""Set default attribute values only
		
		Keyword arguments:
		name -- name of the device (default "")
		vendor -- vendor of the device (default "")
		vendorType -- type of the device for example WS-X6408-G (default "")
		ipv4 -- ipv4 address as a string (default "")
		ipv6 -- ipv6 address as a string (default "")
		serial -- serial number (default "")
		building -- building in which the device is (default "")
		floor -- floor for example 1, E, U (default "")
		room -- room number (default "")
		rack -- rack label f.e. 28.0.15 (default "")
		isMonitored -- device monitoring enabled (default 0)
		"""
		self.deviceName   = name
		self.vendor       = vendor
		self.deviceType   = deviceType
		self.ipv4Address  = ipv4
		self.ipv6Address  = ipv6
		self.serialNumber = serial
		self.building     = building
		self.floor        = floor
		self.room         = room
		self.rack         = rack
		self.isMonitored  = isMonitored

	def toJSON(self):
		"""Return object as JSON

		No arguments
		"""
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

