#!/usr/bin/python
from cnet import * 

apicMap = cNetDataMapperAPICEM("apic.host","user","pass")
apicMap.getUsers()

dev = apicMap.getAllDevices()
print("Found " + str(len(dev)) + " devices")

for einzelnesDev in dev:
	print("Name: " + str(einzelnesDev.deviceName) + " IP: " + str(einzelnesDev.ipv4Address) + " serialNumber " + str(einzelnesDev.serialNumber) + "  isMonitored: " + str(einzelnesDev.isMonitored)   )
