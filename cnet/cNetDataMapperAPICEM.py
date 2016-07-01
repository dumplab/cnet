"""Connection to Cisco APIC-EM - requires requests for REST calls

This class represents the data exchange between APIC-EM and defined objects like cNetDevice. It works best with APIC-EM version > 1.0
"""

__author__    = "dumplab"
__copyright__ = "2016 dumplab"
__license__   = "MIT"
__version__   = "0.5"
__status__    = "Development"

import re,requests,json
requests.packages.urllib3.disable_warnings()
from cNetDevice import cNetDevice

class cNetDataMapperAPICEM:
        """The mapper between APIC-EM and cNetDevices"""

        def __init__(self,host="",user="",passx=""):
		"""Set default attribute values only
		
		Keyword arguments:
		host	= controller hostname or ip address
		user    = username
		pass    = password
		"""
		self.__ticket     = None
		self.__debugging  = False
		# declarations
		self.__GET        = "get"
		self.__POST       = "post"
		# username and password and controller hostname from APIC EM configfile
		self.__controller = host
		self.__username   = user
		self.__password   = passx

	def __getServiceTicket(self):
		"""Get a Service Ticket from APIC-EM"""
		self.__ticket=None
		#specify the username and password which will be included in the data. 
		#your username and password
		payload = {"username":self.__username,"password":self.__password}
  
		#This is the URL to get the service ticket.  
		#The base IP call is https://[Controller IP]/api/v1
		#The REST function is ticket
		url = "https://" + self.__controller + "/api/v1/ticket"
  
		#Content type must be included in the header
		header = {"content-type": "application/json"}
  
		#Format the payload to JSON and add to the data.  Include the header in the call. 
		#SSL certification is turned off, but should be active in production environments
		response= requests.post(url,data=json.dumps(payload), headers=header, verify=False)
  
		#Check if a response was received. If not, print an error message.
		if(not response):
			print ("No data returned!")
		else:
			#Data received.  Get the ticket and print to screen.
			r_json=response.json()
			self.__ticket = r_json["response"]["serviceTicket"]
	#		print ("ticket: ", self.__ticket)

	def __doRestCall(self,aTicket,command,url,aData=None):
		"""__doRestCall
		
		Keyword arguments:
		aTicket -- ticket
		command -- command
		url -- url
		aData -- POST data for example
		"""
		response_json=None
		payload=None
		try:
			#if data for the body is passed in put into JSON format for the payload
			if(aData != None):
				payload=json.dumps(aData)
  
			#add the service ticket and content type to the header
			header = {"X-Auth-Token": aTicket, "content-type" : "application/json"}
			if(command=="get"):
				r = requests.get(url, data=payload, headers=header, verify=False)
			elif(command=="post"):
				r = requests.post(url, data=payload, headers=header, verify=False)
			else:
				#if the command is not GET or POST we dont handle it.
				print ("Unknown command!")
				return
  
			#if no data is returned print a message; otherwise print data to the screen
			if(not r):
				print("No data returned!")
			else:
#				print ("Returned status code: %d" % r.status_code)
				#put into dictionary format
				response_json = r.json()
#				print(response_json)
				return response_json
		except:
			err = sys.exc_info()[0]
			msg_det = sys.exc_info()[1]
#			print( "Error: %s  Details: %s StackTrace: %s" % (err,msg_det,traceback.format_exc()))
			print("Error in restCall")

	def getUsers(self):
		# see if we already got a ticket
		if self.__ticket is None:
	                self.__getServiceTicket()
                #If ticket received get the users
                if(self.__ticket):
       	                #Get user types in the system
			response = self.__doRestCall(self.__ticket,"get", "https://" + self.__controller + "/api/v1/user")
			if self.__debugging == True:
				print("Ticket: " + str(self.__ticket))
				print("Response: " + str(response))

               	else:
               	        print("No service ticket was received.  Ending program!")

	def getAllDevices(self):
		"""getAllDevices - return all APIC-EM device objects of type cNetDevice as a list or None
		
		No arguments
		"""
		# see if we already got a ticket
		if self.__ticket is None:
	                self.__getServiceTicket()
                #If ticket received get devices
                if(self.__ticket):
       	                #Get user types in the system
			response = self.__doRestCall(self.__ticket,"get", "https://" + self.__controller + "/api/v1/network-device")
			if self.__debugging == True:
				print("Ticket: " + str(self.__ticket))
				print("Response: " + str(response))
			# set our parent as the top level response object
			parent = response["response"]
			allDevs = []    # create empty list

			# for each device returned, print the networkDeviceId
			for item in parent:
				allDevs.append(self.__deviceFactory(item))
				if self.__debugging == True:
					print item["hostname"]
					print item["type"]

			return allDevs
               	else:
               	        print("No service ticket was received. Ending program!")

	def getAllConfigs(self):
		"""getAllConfigs - return all Configurations
		
		No arguments
		"""
		# see if we already got a ticket
		if self.__ticket is None:
	                self.__getServiceTicket()
                #If ticket received get the users
                if(self.__ticket):
       	                #Get user types in the system
			response = self.__doRestCall(self.__ticket,"get", "https://" + self.__controller + "/api/v1/network-device/config")
			if self.__debugging == True:
				print("Ticket: " + str(self.__ticket))
				print("Response: " + str(response))
			# set our parent as the top level response object
			parent = response["response"]
			allConfs = []    # create empty list

			# for each device returned, print the networkDeviceId
			for item in parent:
				allConfs.append(item)
#				if self.__debugging == True:
#				print item["runningConfig"]

			return allConfs
               	else:
               	        print("No service ticket was received.  Ending program!")

	def __deviceFactory(self,row):
		"""deviceFactory - return object of type cNetDevice

		Key arguments:
		row -- database row
		"""
#               print("len:" + str(len(row)))
		_device    = row["hostname"]
		_vendor    = "Cisco"
		_type      = row["platformId"]
		_devIp     = row["managementIpAddress"]
		_serial    = row["serialNumber"]
		# fix problem when there is no description
		#dev = cNetDevice(_device,_vendor,_type,str(_devIp),"n/a",_serial,_loc['building'],_loc['floor'],_loc['room'],_loc['rack'],_monitor)
		dev = cNetDevice(_device,_vendor,_type,str(_devIp),"n/a",_serial,)
		# return object
		return dev

if __name__ == '__main__':
	print("This class should only be imported and not run directly!")
