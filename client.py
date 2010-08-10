#!/usr/bin/env python

from gntp.notifier import GrowlNotifier

from gntp.config import Config
from optparse import OptionParser

class ClientConfig(Config):
	_defaults = {
		'gntp':{
			'host':'localhost',
			'port':23053,
			'password':'',
		},
		'client':{
			'appname':'pygntp',
			'name':'Notification Name',
			'title':'Notification Title',
			'priority':0,
			'sticky':False,
			'debug':False,
			'icon':'',
		},
	}
	_booleans = ['client.debug','client.sticky']
	_ints = ['gntp.port','client.priority']
	_editor = True

class ClientParser(OptionParser):
	def __init__(self,file):
		OptionParser.__init__(self)
		self._config = ClientConfig(file)
		
		#Network
		self.add_option("-H","--hostname",
						dest="host",default=self._config['gntp.host'])
		self.add_option("-p","--port",help="port to listen on",
						dest="port",type="int",default=self._config['gntp.port'])
		self.add_option("-P","--password",help="Network password",
					dest='password',default=self._config['server.password'])
		
		#Required (Needs Defaults)
		self.add_option("-a","--appname",
						dest="app",default=self._config['client.appname'])
		self.add_option("-n","--name",
						dest="name",default=self._config['client.name'])
		self.add_option("-t","--title",
						dest="title",default=self._config['client.title'])
		
		#Optional (Does not require Default)
		self.add_option("-d","--debug",help="Print raw growl packets",
						dest='debug',action="store_true",default=self._config['client.debug'])
		self.add_option("-s","--sticky",help="Sticky Notification",
						dest='sticky',action="store_true",default=self._config['client.sticky'])
		self.add_option("--priority",help="-2 to 2  Default 0",
						dest="priority",type="int",default=self._config['client.priority'])
		self.add_option("-i","--icon",help="Icon for notification (Only supports URL currently)",
						dest="icon",default=self._config['client.icon'])
		self.add_option("-e","--edit",help="Open config in $EDITOR",
					dest='edit',action="store_true",default=False)
	def parse_args(self, args=None, values=None):
		values, args = OptionParser.parse_args(self, args, values)
		if values.edit: exit(self._config.editor())
		return values, args

if __name__ == "__main__":
	(options,args) = ClientParser('~/.gntp').parse_args()
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
