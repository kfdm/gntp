#!/usr/bin/env python

from gntp_notifier import GrowlNotifier

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
