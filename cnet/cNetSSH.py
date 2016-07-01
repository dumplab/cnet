"""Generic SSH class providing method to connect switches, routers and other devices using SSHv2.

cNetSSH uses paramiko, see API docs http://docs.paramiko.org/en/latest/ 
"""

__author__    = "dumplab"
__copyright__ = "2015 dumplab"
__license__   = "MIT"
__version__   = "0.5"
__status__    = "Developement"

import paramiko,re,time

class cNetSSH(object):
	"""SSH connection object"""
	
        def __init__(self):
		"""Set default attribute values only
		
		No arguments
		"""
		self.__host      = ""
		self.__user      = ""
		self.__pass      = ""
		self.__conn      = None # paramiko connection
		self.__shell     = None # when using a channel
		self.__connected = False
		self.__input     = ""
		self.__output    = ""
		self.__timeout   = 1.0  # right now we use a timeout of 2 seconds to connect
		self.__outEnd    = ""   # will be considered as the prompt and end of an output see recv is discovered during the login
		self.__debug     = False

	def connect(self,hostName,userName="",userPass="",newShell=True,paging=False):
		"""connect a device using provided credentials and start an interactive shell
		
		Keyword arguments:
		hostName = hostname (default "")
		userName = username to authenticate (default "")
		userPass = password to use for authenticating and for unlocking a private key (default "")
		newShell = shall we start a shell, opens a new Channel (default True)
		paging   = enable or disable paging/more (Default False)
		returns the configuration as a string
		"""
		self.__host = hostName
		self.__user = userName
		self.__pass = userPass

		try:
			self.__conn = paramiko.SSHClient()
			# add untrusted hosts
			self.__conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			# connect to host
			self.__conn.connect(self.__host,username=self.__user,password=self.__pass,timeout=1.0)
			# set connected flag
			self.__connected = True
			# debug
			if self.__debug:
				print("cNetSSH::connect - connected to device " + self.__outEnd)
			# Start an interactive shell session on the SSH server. A new Channel is opened and connected to a pseudo-terminal using the requested terminal type and size.
			if newShell==True:
				self.__shell = self.__conn.invoke_shell()
				time.sleep(0.3)
				# Save the initial router prompt
				self.__output = self.__shell.recv(32000)
				self.__output = self.__output.splitlines(True)
				self.__outEnd = self.__output[len(self.__output)-1]
				if self.__debug:
					print("cNetSSH::connect - I'll consider this string as the prompt in further requests: " + self.__outEnd)
				if paging==False:
					self.__disablePaging()
		except paramiko.AuthenticationException:
			print("Authentication failed when connecting to " + self.__host)
			sys.exit(1)
		except:
			print("Could not connect to host " + self.__host)


	def enable(self,password=""):
		"""enable - enter enable mode. please use this method as it stores the new prompt to spped up futher command processing
		
		Keyword arguments:
		password = enable password (default "")
		"""
		if self.__connected:
			self.__input = "enable"
			numBytes     = self.__shell.send(self.__input + "\n" + password + "\n")
			if numBytes > 0:
				time.sleep(0.3)
				# Save the router prompt
				self.__output = self.__shell.recv(32000)
				self.__output = self.__output.splitlines(True)
				self.__outEnd = self.__output[len(self.__output)-1]
				if self.__debug:
					print("cNetSSH::enable - change expected prompt to " + self.__outEnd)
				return True
		else:
			print("Not connected to " + self.__host + ". Connect first.")

	def send(self,command):
		if self.__connected:
			self.__input = command
			numBytes     = self.__shell.send(command + "\n")
			if numBytes > 0:
				self.__output = ""
				myTempBuffer  = ""
				max_try       = 500
				x             = 0
				sTime         = time.time()
				bailedOut     = False
				while x < max_try:
					if self.__shell.recv_ready():
						if self.__debug:
							print("cNetSSH::send - recv_ready() on cycle=" + str(x))
						while True:
							# note recv returns if there is > 0 < 1024
							myTempBuffer = self.__shell.recv(1024)
							self.__output += myTempBuffer
							#print("cNetSSH: recv() returned ... len=" + str(len(myTempBuffer)))
							if len(myTempBuffer)==0 or self.__shell.recv_ready()==False:
								break
					else:
						time.sleep(0.00005)
					x += 1
					# bail out if we've found the prompt again
					if re.search(self.__outEnd,self.__output):
						bailedOut = True
						break
				if self.__debug:
					eTime = time.time()-sTime
					print("cNetSSH::send - received " + str(len(self.__output)) + " bytes in " + str(x) + " cycles and " + str(eTime) + "s. BailedOut: " + str(bailedOut))
				return self.__sanitizeOutput(self.__output)
		else:
			print("Not connected to " + self.__host + ". Connect first.")

	def disconnect(self):
		"""disconnect
		
		returns the configuration as a string
		"""
		self.__conn = None

	def __sanitizeOutput(self,output):
		"""sanitizeOutput - remove the sent command from output and the prompt
		
		returns the configuration as a string
		"""
		tempOut = output.splitlines(True)
		newOut  = ""
		for line in tempOut:
			if not re.search("^" + self.__outEnd,line) and not re.search(self.__input,line):
				newOut += line
		return newOut

	def __disablePaging(self):
		if self.__connected:
			self.__shell.send("terminal length 0\n")
			time.sleep(0.25)
			if self.__shell.recv_ready():
				self.__output = self.__shell.recv(200)
		else:
			print("Not connected to " + self.__host + ". Connect first.")

	def configure(self):
		"""enter configuration mode using configure terminal
		
		returns True on success, False on problems
		"""
		if self.__connected:
			self.__shell.send("\nconfigure terminal\n")
			time.sleep(0.25)
			if self.__shell.recv_ready():
				self.__output = self.__shell.recv(200)
				# we expect (config)#
				if re.search("config\)#",self.__output):
					return True
				return False
		else:
			print("Not connected to " + self.__host + ". Connect first.")
			return False

	def noconfigure(self):
		"""leave configuration mode using configure terminal
		
		returns True on success, False on problems
		"""
		if self.__connected:
			self.__shell.send("\nend\n")
			time.sleep(0.25)
			if self.__shell.recv_ready():
				self.__output = self.__shell.recv(200)
				# we expect (config)#
				if re.search("#",self.__output):
					return True
				return False
		else:
			print("Not connected to " + self.__host + ". Connect first.")
			return False

if __name__ == '__main__':
	print("This class should only be imported and not run directly!")
