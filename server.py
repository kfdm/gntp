import SocketServer
import traceback
import time

class GNTPServer(SocketServer.TCPServer):
	pass

class GNTPHandler(SocketServer.StreamRequestHandler):
	def read(self):
		bufferSleep = 0.01
		bufferLength = 2048
		time.sleep(bufferSleep) #Let the buffer fill up a bit (hack)
		buffer = ''
		while(1):
			data = self.request.recv(bufferLength)
			if self.server.growl_debug:
				print 'Reading',len(data)
			buffer = buffer + data
			if len(data) < bufferLength: break
			time.sleep(bufferSleep) #Let the buffer fill up a bit (hack)
		if self.server.growl_debug:
			print '<Reading>\n',buffer,'\n</Reading>'
		return buffer
	def write(self,msg):
		if self.server.growl_debug:
			print '<Writing>\n',msg,'\n</Writing>'
		self.request.send(msg)
	def handle(self):
		reload(gntp)
		self.data = self.read()
		
		try:
			message = gntp.parse_gntp(self.data,self.server.growl_password)
			message.send()
			
			response = gntp.GNTPOK(action=message.info['messagetype'])
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
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-a","--address",dest="host",help="address to listen on",default="")
	parser.add_option("-p","--port",dest="port",help="port to listen on",type="int",default=23053)
	parser.add_option("-r","--regrowl",dest='regrowl',help="ReGrowl on local OSX machine",action="store_true",default=False)
	parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
	parser.add_option("-P","--password",dest='password',help="Network password",default=None)
	(options, args) = parser.parse_args()
	
	if options.regrowl:
		import gntp_bridge as gntp
	else:
		import gntp
	
	server = GNTPServer((options.host, options.port), GNTPHandler)
	server.growl_debug = options.debug
	server.growl_password = options.password
	
	sa = server.socket.getsockname()
	print "Listening for GNTP on", sa[0], "port", sa[1], "..."
	server.serve_forever()
