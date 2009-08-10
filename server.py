import SocketServer
import re
import gntp

class GNTPServer(SocketServer.TCPServer):
	pass

class GNTPHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024)
		
		if re.match('GNTP/1.0 REGISTER', self.data):
			reload(gntp)
			print "%s sent REGISTER:" % self.client_address[0]
			tmp = gntp.GNTPRegister(self.data)
		elif re.match('GNTP/1.0 NOTIFY', self.data):
			reload(gntp)
			print "%s sent NOTIFY:" % self.client_address[0]
			tmp = gntp.GNTPNotice(self.data)
		else:
			print "%s sent UNKNOWN:" % self.client_address[0]
			print '----'
			print self.data
			print '----'
			return None
		tmp.send()
		
if __name__ == "__main__":
	HOST,PORT = '',23053
	
	server = GNTPServer((HOST, PORT), GNTPHandler)
	
	sa = server.socket.getsockname()
	print "Listening for GNTP on", sa[0], "port", sa[1], "..."
	server.serve_forever()
	