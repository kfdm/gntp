import gntp
import socket
import sys

def send_growl(options,message=None):
	#Send Registration
	register = gntp.GNTPRegister()
	register.add_header('Application-Name',options.app)
	register.add_notification(options.name,True)
	
	if options.password:
		register.set_password(options.password)
	
	_send(options.host,options.port,register.encode(),options.debug)
	
	#Send Notification
	notice = gntp.GNTPNotice()
	
	#Required
	notice.add_header('Application-Name',options.app)
	notice.add_header('Notification-Name',options.name)
	notice.add_header('Notification-Title',options.title)
	
	if options.password:
		notice.set_password(options.password)

	#Optional
	if options.sticky:
		notice.add_header('Notification-Sticky',options.sticky)
	if options.priority:
		notice.add_header('Notification-Priority',options.priority)
	
	if message:
		notice.add_header('Notification-Text',message)
	
	_send(options.host,options.port,notice.encode(),options.debug)

def _send(host,port,data,debug=False):
	if debug: print '-----\n',data,'\n----'
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.send(data)
	response = s.recv(1024)
	s.close()
	
	if debug: print '-----\n',response,'\n----'

if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser(usage="usage: %prog [options] message")
	
	#Network
	parser.add_option("-H","--hostname",dest="host",default="localhost")
	parser.add_option("-p","--port",dest="port",help="port to listen on",type="int",default=23053)
	parser.add_option("-P","--password",dest="password",help="network password")

	#Required (Needs Defaults)
	parser.add_option("-a","--appname",dest="app",default="pygntp")
	parser.add_option("-n","--name",dest="name",default="Notification Name")
	parser.add_option("-t","--title",dest="title",default="Notification Title")
	
	#Optional (Does not require Default)
	parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
	parser.add_option("-s","--sticky",dest='sticky',help="Sticky Notification",action="store_true",default=None)
	parser.add_option("--priority",dest="priority",help="-2 to 2  Default 0",type="int",default=None)
	
	(options, args) = parser.parse_args()
	if len(args) > 0:
		send_growl(options,' '.join(args))
	else:
		send_growl(options)
