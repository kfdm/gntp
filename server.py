import SocketServer
import local
import gntp

class GNTPServer(SocketServer.TCPServer):
	pass

class GNTPHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024)
		
		if self.data.startswith('GNTP/1.0 REGISTER'):
			reload(local)
			print "%s sent REGISTER:" % self.client_address[0]
			local.GNTPRegister(self.data).send()
			self.request.send(gntp.GNTPResponse().format())
		elif self.data.startswith('GNTP/1.0 NOTIFY'):
			reload(local)
			print "%s sent NOTIFY:" % self.client_address[0]
			local.GNTPNotice(self.data).send()
			self.request.send(gntp.GNTPResponse().format())
		else:
			print "%s sent UNKNOWN:" % self.client_address[0]
			print '----'
			print self.data
			print '----'
			return None
		
if __name__ == "__main__":
	HOST,PORT = '',23053
	
	server = GNTPServer((HOST, PORT), GNTPHandler)
	
	sa = server.socket.getsockname()
	print "Listening for GNTP on", sa[0], "port", sa[1], "..."
	server.serve_forever()
	