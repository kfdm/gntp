import re

class GNTPBase(object):
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

class GNTPRegister(GNTPBase):
	def __init__(self,data=None):
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
			self.parse(data)
		else:
			self.headers['Application-Name'] = 'pygntp'
			self.headers['Notifications-Count'] = 0
	def validate(self):
		for header in self.requiredHeaders:
			if not self.headers.get(header,False):
				raise Exception('Missing Registration Header: '+header)
		for notice in self.notifications:
			for header in self.requiredNotification:
				if not notice.get(header,False):
					raise Exception('Missing Notification Header: '+header)		
	def parse(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
		
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
	def format(self):
		self.validate()
		SEP = u': '
		EOL = u'\r\n'
		
		message = u'GNTP/1.0 REGISTER NONE ' + EOL
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
		print self.format()

class GNTPNotice(GNTPBase):
	def __init__(self,data=None,app=None,name=None,title=None):
		self.raw	= data
		self.headers	= {}
		self.resources	= {}
		self.requiredHeaders = [
			'Application-Name',
			'Notification-Name',
			'Notification-Title'
		]
		if data:
			self.parse(data)
		else:
			if app:
				self.headers['Application-Name'] = app
			if name:
				self.headers['Notification-Name'] = name
			if title:
				self.headers['Notification-Title'] = title
	def validate(self):
		for header in self.requiredHeaders:
			print self.headers
			if not self.headers.get(header,False):
				raise Exception('Missing Notification Header: '+header)
	def parse(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
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
		print self.format()
	def format(self):
		SEP = u': '
		EOL = u'\r\n'
		
		message = u'GNTP/1.0 NOTIFY NONE ' + EOL
		#Headers
		for k,v in self.headers.iteritems():
			message += k.encode('utf8') + SEP + str(v).encode('utf8') + EOL
		
		message += EOL
		return message

class GNTPResponse(object):
	def format(self):
		return 'GNTP/1.0 -OK NONE\r\n\r\n'