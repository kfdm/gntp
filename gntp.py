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
		

class GNTPRegister(GNTPBase):
	def __init__(self,data=None):
		self.headers	= {}
		self.notifications = []
		self.defaultNotifications = []
		if data:
			self.parse(data)
	def parse(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
		
		self.headers = self.parse_dict(parts[0])
		
		if len(parts) > 1:
			for notification in parts[1:]:
				if notification.strip()=='': continue
				notice = self.parse_dict(notification)
				self.notifications.append(notice['Notification-Name'])
				if notice['Notification-Enabled'] == 'True':
					self.defaultNotifications.append(notice['Notification-Name'])
				
	def __unicode__(self):
		return self.headers
	def send(self):
		print
		print '=Registration Object='
		print '==Headers=='
		print self.headers
		print '==Notifications=='
		print self.notifications
		print '==Defaults=='
		print self.defaultNotifications
		print

class GNTPNotice(GNTPBase):
	def __init__(self,data=None):
		self.raw	= data
		self.headers	= {}
		self.resources	= {}
		if data:
			self.parse(data)
	def parse(self,data):
		self.raw = data
		parts = self.raw.split('\r\n\r\n')
		self.headers = self.parse_dict(parts[0])
		if len(parts) > 1:
			print parts[1:]
			if parts[1] == '': return
			item					= self.parse_dict(parts[1])
			#print len(parts[2])
			#print parts[2]
			item['Data']			= parts[2]
			self.resources[item['Identifier']] = item
			
	def send(self):
		print
		print '=Notification Object='
		print '==Headers=='
		print self.headers
		print '==Resources=='
		print self.resources
		print
			
	def __unicode__(self):
		return self.headers

class GNTPResponse(object):
	def format(self):
		return 'GNTP/1.0 -OK NONE\r\n\r\n'