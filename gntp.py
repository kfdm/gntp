import re
import hashlib
import time

class GNTPParseError(Exception):
	pass

class _GNTPBase(object):
	def __init__(self,messagetype):
		self.info = {
			'version':'1.0',
			'messagetype':messagetype,
			'encryptionAlgorithmID':None
		}
	def parse_info(self,data):
		#GNTP/<version> <messagetype> <encryptionAlgorithmID>[:<ivValue>][ <keyHashAlgorithmID>:<keyHash>.<salt>]
		match = re.match('GNTP/(?P<version>\d+\.\d+) (?P<messagetype>REGISTER|NOTIFY|\-OK|\-ERROR)'+
						' (?P<encryptionAlgorithmID>[A-Z0-9]+(:(?P<ivValue>[A-F0-9]+))?) ?'+
						'((?P<keyHashAlgorithmID>[A-Z0-9]+):(?P<keyHash>[A-F0-9]+).(?P<salt>[A-F0-9]+))?\r\n', data,re.IGNORECASE)
		
		if not match:
			raise GNTPParseError('ERROR_PARSING_INFO_LINE')
		
		info = match.groupdict()
		if info['encryptionAlgorithmID'] == 'NONE':
			info['encryptionAlgorithmID'] = None
		
		return info
	def set_password(self,password,encryptAlgo='MD5'):
		password = password.encode('utf8')
		seed = time.ctime()
		salt = hashlib.md5(seed).hexdigest()
		saltHash = hashlib.md5(seed).digest()
		keyBasis = password+saltHash
		key = hashlib.md5(keyBasis).digest()
		keyHash = hashlib.md5(key).hexdigest()
				
		self.info['keyHashAlgorithmID'] = encryptAlgo.upper()
		self.info['keyHash'] = keyHash.upper()
		self.info['salt'] = salt.upper()
		
	def format_info(self):
		info = u'GNTP/%s %s'%(
			self.info.get('version'),
			self.info.get('messagetype'),
		)
		if self.info.get('encryptionAlgorithmID',None):
			info += ' %s:%s'%(
				self.info.get('encryptionAlgorithmID'),
				self.info.get('ivValue'),
			)
		else:
			info+=' NONE'
		
		if self.info.get('keyHashAlgorithmID',None):
			info += ' %s:%s.%s'%(
				self.info.get('keyHashAlgorithmID'),
				self.info.get('keyHash'),
				self.info.get('salt')
			)			
		
		return info	
	def parse_dict(self,data):
		dict = {}
		for line in data.split('\r\n'):
			match = re.match('([\w-]+):(.+)', line)
			if not match: continue
			
			key = match.group(1).strip()
			val = match.group(2).strip()
			dict[key] = val
			#print key,'\t\t\t',val
		return dict
	def add_header(self,key,value):
		self.headers[key] = value

class GNTPRegister(_GNTPBase):
	def __init__(self,data=None):
		_GNTPBase.__init__(self,'REGISTER')
		self.headers	= {}
		self.notifications = []
		self.requiredHeaders = [
			'Application-Name',
			'Notifications-Count'
		]
		self.requiredNotification = [
			'Notification-Name',
		]
		if data:
			self.decode(data)
		else:
			self.headers['Application-Name'] = 'pygntp'
			self.headers['Notifications-Count'] = 0
	def validate(self):
		for header in self.requiredHeaders:
			if not self.headers.get(header,False):
				raise GNTPParseError('Missing Registration Header: '+header)
		for notice in self.notifications:
			for header in self.requiredNotification:
				if not notice.get(header,False):
					raise GNTPParseError('Missing Notification Header: '+header)		
	def decode(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
		self.info = self.parse_info(data)
		self.headers = self.parse_dict(parts[0])
		
		if len(parts) > 1:
			for notification in parts[1:]:
				if notification.strip()=='': continue
				notice = self.parse_dict(notification)
				self.notifications.append(notice)
	def add_notification(self,name,enabled=True):
		notice = {}
		notice['Notification-Name'] = name
		notice['Notification-Enabled'] = str(enabled)
			
		self.notifications.append(notice)
		self.headers['Notifications-Count'] = len(self.notifications)
	def encode(self):
		self.validate()
		SEP = u': '
		EOL = u'\r\n'
		
		message = self.format_info() + EOL
		#Headers
		for k,v in self.headers.iteritems():
			message += k.encode('utf8') + SEP + str(v).encode('utf8') + EOL
		
		#Notifications
		if len(self.notifications)>0:
			for notice in self.notifications:
				message += EOL
				for k,v in notice.iteritems():
					message += k.encode('utf8') + SEP + str(v).encode('utf8') + EOL
		
		message += EOL
		return message
	
	def send(self):
		print self.encode()
	def __str__(self):
		return self.encode()

class GNTPNotice(_GNTPBase):
	def __init__(self,data=None,app=None,name=None,title=None):
		_GNTPBase.__init__(self,'NOTIFY')
		self.headers	= {}
		self.resources	= {}
		self.requiredHeaders = [
			'Application-Name',
			'Notification-Name',
			'Notification-Title'
		]
		if data:
			self.decode(data)
		else:
			if app:
				self.headers['Application-Name'] = app
			if name:
				self.headers['Notification-Name'] = name
			if title:
				self.headers['Notification-Title'] = title
	def validate(self):
		for header in self.requiredHeaders:
			if not self.headers.get(header,False):
				raise GNTPParseError('Missing Notification Header: '+header)
	def decode(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
		self.info = self.parse_info(data)
		self.headers = self.parse_dict(parts[0])
		if len(parts) > 1:
			print 'Extra parts'
			print parts[1:]
			if parts[1] == '': return
			item					= self.parse_dict(parts[1])
			#print len(parts[2])
			#print parts[2]
			item['Data']			= parts[2]
			self.resources[item['Identifier']] = item
			
	def send(self):
		print self.encode()
	def __str__(self):
		return self.encode()
	def encode(self):
		self.validate()
		SEP = u': '
		EOL = u'\r\n'
		
		message = self.format_info() + EOL
		#Headers
		for k,v in self.headers.iteritems():
			message += k.encode('utf8') + SEP + str(v).encode('utf8') + EOL
		
		message += EOL
		return message

class GNTPResponse(_GNTPBase):
	def __init__(self,type='-OK'):
		_GNTPBase.__init__(self,type)
		self.headers = {}
	def decode(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
		self.info = self.parse_info(data)
		self.headers = self.parse_dict(parts[0])
	def encode(self):
		#self.validate()
		SEP = u': '
		EOL = u'\r\n'
		
		message = self.format_info() + EOL
		#Headers
		for k,v in self.headers.iteritems():
			message += k.encode('utf8') + SEP + str(v).encode('utf8') + EOL
		
		message += EOL
		return message
	def send(self):
		print self.encode()
	def __str__(self):
		return self.encode()

class GNTPOK(GNTPResponse):
	def __init__(self,data=None):
		GNTPResponse.__init__(self,'-OK')
		if data:
			self.decode(data)

class GNTPError(GNTPResponse):
	def __init__(self,data=None):
		GNTPResponse.__init__(self,'-ERROR')
		if data:
			self.decode(data)

def parse_gntp(data,debug=False):
	match = re.match('GNTP/(?P<version>\d+\.\d+) (?P<messagetype>REGISTER|NOTIFY|\-OK|\-ERROR)',data,re.IGNORECASE)
	if not match:
		raise GNTPParseError('INVALID_GNTP_INFO')
	info = match.groupdict()
	if info['messagetype'] == 'REGISTER':
		return GNTPRegister(data)
	elif info['messagetype'] == 'NOTICE':
		return GNTPNotice(data)
	elif info['messagetype'] == '-OK':
		return GNTPResponse(data)
	elif info['messagetype'] == '-ERROR':
		return GNTPResponse(data)
	if debug:
		print '----'
		print self.data
		print '----'
	raise GNTPParseError('INVALID_GNTP_MESSAGE')
