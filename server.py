import SocketServer
import traceback

class GNTPServer(SocketServer.TCPServer):
	pass

class GNTPHandler(SocketServer.StreamRequestHandler):
	def read(self):
		data = self.request.recv(1024)
		if self.server.growl_debug:
			print '---'
			print data
			print '---'
		return data
	def write(self,msg):
		if self.server.growl_debug:
			print '---'
			print msg
			print '---'
		self.request.send(msg)
	def handle(self):
		self.data = self.read()
		
		try:
			message = gntp.parse_gntp(self.data,self.server.growl_password)
			message.send()
			
			response = gntp.GNTPOK()
			self.write(response.encode())
		except gntp.GNTPError:
			if self.server.growl_debug:
				traceback.print_exc()
			response = gntp.GNTPError()
			self.write(response.encode())
		
if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-a","--address",dest="host",help="address to listen on",default="")
	parser.add_option("-p","--port",dest="port",help="port to listen on",type="int",default=23053)
	parser.add_option("-r","--regrowl",dest='regrowl',help="ReGrowl on local OSX machine",action="store_true",default=False)
	parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
	parser.add_option("-P","--password",dest='password',help="Network password",default=None)
	(options, args) = parser.parse_args()
	
	if options.regrowl:
		import local as gntp
	else:
		import gntp
	
	server = GNTPServer((options.host, options.port), GNTPHandler)
	server.growl_debug = options.debug
	server.growl_password = options.password
	
	sa = server.socket.getsockname()
	print "Listening for GNTP on", sa[0], "port", sa[1], "..."
	server.serve_forever()
	