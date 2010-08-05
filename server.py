#!/usr/bin/env python

import SocketServer
import traceback
import time
from gntp.config import Config
from optparse import OptionParser

class ServerConfig(Config):
	_defaults = {
		'gntp':{
			'host':'localhost',
			'port':23053,
			'password':'',
		},
		'server':{
			'address':'',
			'port':23053,
			'password':'',
			'regrowl':False,
			'debug':False,
		},
	}
	_booleans = ['server.debug','server.regrowl']
	_ints = ['gntp.port','server.port']
	_editor = True
	
class ServerParser(OptionParser):
	def __init__(self,file):
		OptionParser.__init__(self)
		self._config = ServerConfig(file)
		
		# Network Options		
		self.add_option("-a","--address",help="address to listen on",
					dest="host",default=self._config['server.address'])
		self.add_option("-p","--port",help="port to listen on",
					dest="port",type="int",default=self._config['server.port'])
		self.add_option("-P","--password",help="Network password",
					dest='password',default=self._config['server.password'])
		
		# Misc Options
		self.add_option("-r","--regrowl",help="ReGrowl on local OSX machine",
					dest='regrowl',action="store_true",default=self._config['server.regrowl'])
		
		# Debug Options
		self.add_option("-d","--debug",help="Print raw growl packets",
					dest='debug',action="store_true",default=self._config['server.debug'])
		self.add_option("-q","--quiet",help="Quiet mode",
					dest='debug',action="store_false")

class GNTPServer(SocketServer.TCPServer):
	def serve_forever(self):
		if self.growl_debug:
			sa = self.socket.getsockname()
			print "Listening for GNTP on", sa[0], "port", sa[1], "..."
		SocketServer.TCPServer.serve_forever(self)

class GNTPHandler(SocketServer.StreamRequestHandler):
	def read(self):
		bufferLength = 2048
		buffer = ''
		while(1):
			data = self.request.recv(bufferLength)
			if self.server.growl_debug:
				print 'Reading',len(data)
			buffer = buffer + data
			if len(data) < bufferLength and buffer.endswith('\r\n\r\n'):
				break
		if self.server.growl_debug:
			print '<Reading>\n',buffer,'\n</Reading>'
		return buffer
	def write(self,msg):
		if self.server.growl_debug:
			print '<Writing>\n',msg,'\n</Writing>'
		self.request.sendall(msg)
	def handle(self):
		reload(gntp)
		self.data = self.read()
		
		try:
			message = gntp.parse_gntp(self.data,self.server.growl_password)
			message.send()
			
			response = gntp.GNTPOK(action=message.info['messagetype'])
			if message.info['messagetype'] == 'NOTICE':
				response.add_header('Notification-ID','')
			elif message.info['messagetype'] == 'SUBSCRIBE':
				raise gntp.UnsupportedError()
				#response.add_header('Subscription-TTL','10')
			self.write(response.encode())
		except gntp.BaseError, e:
			if self.server.growl_debug:
				traceback.print_exc()
			if e.gntp_error:
				self.write(e.gntp_error())
		except:
			error = gntp.GNTPError(errorcode=500,errordesc='Unknown server error')
			self.write(error.encode())
			raise
		
if __name__ == "__main__":
	(options,args) = ServerParser('~/.gntp').parse_args()
	
	if options.regrowl:
		import gntp_bridge as gntp
	else:
		import gntp
	
	server = GNTPServer((options.host, options.port), GNTPHandler)
	server.growl_debug = options.debug
	server.growl_password = options.password
	
	server.serve_forever()
