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
			message = parse_gntp(self.data)
			message.send()
			
			response = GNTPOK()
			self.write(response.encode())
		except GNTPError:
			if self.server.growl_debug:
				traceback.print_exc()
			response = GNTPError()
			self.write(response.encode())
		
if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-a","--address",dest="host",help="address to listen on",default="")
	parser.add_option("-p","--port",dest="port",help="port to listen on",type="int",default=23053)
	parser.add_option("-r","--regrowl",dest='regrowl',help="ReGrowl on local OSX machine",action="store_true",default=False)
	parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
	(options, args) = parser.parse_args()
	
	if options.regrowl:
		from local import GNTPRegister,GNTPNotice
		from gntp import GNTPParseError,GNTPOK,GNTPError,parse_gntp
	else:
		from gntp import *
	
	server = GNTPServer((options.host, options.port), GNTPHandler)
	server.growl_debug = options.debug
	
	sa = server.socket.getsockname()
	print "Listening for GNTP on", sa[0], "port", sa[1], "..."
	server.serve_forever()
	