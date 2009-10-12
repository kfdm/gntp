import SocketServer
import traceback
import time

class GNTPServer(SocketServer.TCPServer):
	pass

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

def send_subscribe(options):
	options.debug = True
	subscribe = gntp.GNTPSubscribe(password=options.password)
	subscribe.add_header('Subscriber-ID',platform.node())
	subscribe.add_header('Subscriber-Name',platform.node())
	subscribe.add_header('Subscriber-Port',options.port)
	
	data = subscribe.encode()
	
	if options.debug: print '<Sending>\n',data,'\n</Sending>'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((options.subscribe,options.remote_port))
	s.send(data)
	response = gntp.parse_gntp(s.recv(1024))
	s.close()
	if options.debug: print '<Recieved>\n',response,'\n</Recieved>'
	
	try: ttl = int(response.headers['Subscription-TTL']) - 30
	except: ttl = 0
	
	if ttl <= 0: raise gntp.BaseError('Error with subscribe message')
	
	if options.debug: print 'Resubscribing in',ttl,'seconds'
	threading.Timer(ttl,send_subscribe,[options]).start()
	
if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-a","--address",dest="host",help="address to listen on",default="")
	parser.add_option("-p","--port",dest="port",help="port to listen on",type="int",default=23053)
	parser.add_option("-r","--regrowl",dest='regrowl',help="ReGrowl on local OSX machine",action="store_true",default=False)
	parser.add_option("-d","--debug",dest='debug',help="Print raw growl packets",action="store_true",default=False)
	parser.add_option("-P","--password",dest='password',help="Network password",default=None)
	parser.add_option("-s","--subscribe",dest='subscribe',help="Subscribe to a remote server",default=None)
	parser.add_option("--remote-port",dest='remote_port',help="Port on the remote machine",type="int",default=23053)
	(options, args) = parser.parse_args()
	
	if options.regrowl:
		import gntp_bridge as gntp
	else:
		import gntp
	
	server = GNTPServer((options.host, options.port), GNTPHandler)
	server.growl_debug = options.debug
	server.growl_password = options.password
	
	if options.subscribe:
		import threading
		import platform
		import socket
		print 'Subscribing to: ',options.subscribe,':',options.remote_port
		threading.Timer(1.0,send_subscribe,[options]).start()
	
	sa = server.socket.getsockname()
	print "Listening for GNTP on", sa[0], "port", sa[1], "..."
	server.serve_forever()
