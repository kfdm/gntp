#!/usr/bin/env python
"""
A Python module that uses GNTP to post messages
Mostly mirrors the Growl.py file that comes with Mac Growl
http://code.google.com/p/growl/source/browse/Bindings/python/Growl.py
"""
import gntp
import socket

class GrowlNotifier(object):
	applicationName = 'Python GNTP'
	notifications = []
	defaultNotifications = []
	applicationIcon = None
	
	#GNTP Specific
	debug = False
	password = None
	hostname = None
	port = 23053
	
	def __init__(self, applicationName=None, notifications=None, defaultNotifications=None, applicationIcon=None, hostname=None, password=None, port=None, debug=False):
		if applicationName:
			self.applicationName = applicationName
		assert self.applicationName, 'An application name is required.'

		if notifications:
			self.notifications = list(notifications)
		assert self.notifications, 'A sequence of one or more notification names is required.'

		if defaultNotifications is not None:
			self.defaultNotifications = list(defaultNotifications)
		elif not self.defaultNotifications:
			self.defaultNotifications = list(self.notifications)

		if applicationIcon is not None:
			self.applicationIcon = self._checkIcon(applicationIcon)
		elif self.applicationIcon is not None:
			self.applicationIcon = self._checkIcon(self.applicationIcon)
		
		#GNTP Specific
		if password:
			self.password = password
		
		if hostname:
			self.hostname = hostname
		assert self.hostname, 'Requires valid hostname'
		
		if port:
			self.port = int(port)
		assert isinstance(self.port,int), 'Requires valid port'
		
		if debug:
			self.debug = debug
		
	def _checkIcon(self, data):
		'''
		Check the icon to see if it's valid
		@param data: 
		@todo Consider checking for a valid URL
		'''
		return data
	
	def register(self):
		'''
		Send GNTP Registration
		'''
		register = gntp.GNTPRegister()
		register.add_header('Application-Name',self.applicationName)
		for notification in self.notifications:
			enabled = notification in self.defaultNotifications
			register.add_notification(notification,enabled)
		if self.password:
			register.set_password(self.password)
		self.send(register.encode())
	
	def notify(self, noteType, title, description, icon=None, sticky=False, priority=None):
		'''
		Send a GNTP notifications
		'''
		assert noteType in self.notifications
		notice = gntp.GNTPNotice()
		notice.add_header('Application-Name',self.applicationName)
		notice.add_header('Notification-Name',noteType)
		notice.add_header('Notification-Title',title)
		if self.password:
			notice.set_password(self.password)
		if sticky:
			notice.add_header('Notification-Sticky',sticky)
		if priority:
			notice.add_header('Notification-Priority',priority)
		if icon:
			notice.add_header('Notification-Icon',self._checkIcon(icon))
		if description:
			notice.add_header('Notification-Text',description)
		self.send(notice.encode())
	def send(self,data):
		'''
		Send the GNTP Packet
		'''
		if self.debug: print '<Sending>\n',data,'\n</Sending>'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.hostname,self.port))
		s.send(data)
		response = gntp.parse_gntp(s.recv(1024))
		s.close()
		if self.debug: print '<Recieved>\n',response,'\n</Recieved>'

if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser(usage="usage: %prog [options] message")
	
	#Network
	parser.add_option("-H","--hostname",dest="host",default="localhost")
	parser.add_option("-p","--port",dest="port",help="port to listen on",type="int",default=23053)
	parser.add_option("-P","--password",dest="password",default=None,help="network password")

	#Required (Needs Defaults)
	parser.add_option("-a","--appname",dest="app",default="pygntp")
	parser.add_option("-n","--name",dest="name",default="Notification Name")
	parser.add_option("-t","--title",dest="title",default="Notification Title")
	
	#Optional (Does not require Default)
	parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
	parser.add_option("-s","--sticky",dest='sticky',help="Sticky Notification",action="store_true",default=None)
	parser.add_option("--priority",dest="priority",help="-2 to 2  Default 0",type="int",default=None)
	parser.add_option("-i","--icon",dest="icon",help="Icon for notification (Only supports URL currently)",default=False)
	
	(options, args) = parser.parse_args()
	if len(args) > 0: message = ' '.join(args)
	else: message = ''
	
	growl = GrowlNotifier(
		applicationName = options.app,
		notifications = [options.name],
		defaultNotifications = [options.name],
		hostname = options.host,
		password = options.password,
		port = options.port,
		debug = options.debug,
	)
	growl.register()
	growl.notify(
		noteType = options.name,
		title = options.title,
		description = message,
		icon = options.icon,
		sticky = options.sticky,
		priority = options.priority,
	)
