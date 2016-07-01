#!/usr/bin/python
# Required classes
from cnet import *

# instantiate the SSH object so we can loging using ssh
device = cNetSSH()
# connect to an SSH enabled switch or router
device.connect("172.2.2.24","username","password")
# optiona enable
#device.enable("pass")
# send show version
out = device.send("show version")
# print output
print(out)
