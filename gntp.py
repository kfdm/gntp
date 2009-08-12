import re
import Growl

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
	def __init__(self,data):
		self.raw	= data
		self.parsed	= {}
		self.notifications = []
		self.defaultNotifications = []
		self.parse()
	def parse(self):
		parts = self.raw.split('\r\n\r\n')
		
		self.parsed = self.parse_dict(parts[0])
		
		if len(parts) > 1:
			self.parsed['notification'] = []
			self.parsed['defaultNotifications'] = []
			for notification in parts[1:]:
				if notification.strip()=='': continue
				notice = self.parse_dict(notification)
				self.notifications.append(notice['Notification-Name'])
				if notice['Notification-Enabled'] == 'True':
					self.defaultNotifications.append(notice['Notification-Name'])
				
	def __unicode__(self):
		return self.parsed
	def send(self):
		print 'Sending Registration'
		growl = Growl.GrowlNotifier(
			applicationName			= self.parsed['Application-Name'],
			notifications			= self.notifications,
			defaultNotifications	= self.defaultNotifications,
		)
		growl.register()

class GNTPNotice(GNTPBase):
	def __init__(self,data):
		self.raw	= data
		self.parsed	= {}
		self.parse()
	def parse(self):
		parts = self.raw.split('\r\n\r\n')
		self.parsed = self.parse_dict(parts[0])
		if len(parts) > 1:
			self.parsed['identifier'] = {}
			item					= self.parse_dict(parts[1])
			#print len(parts[2])
			#print parts[2]
			item['Data']			= parts[2]
			self.parsed['identifier'][item['Identifier']] = item
			
	def send(self):
		print 'Sending Notification'
		growl = Growl.GrowlNotifier(
			applicationName			= self.parsed['Application-Name'],
			notifications			= [self.parsed['Notification-Name']]
		)
		
		noticeIcon = None
		if self.parsed.get('Notification-Icon',False):
			resource = self.parsed['Notification-Icon'].split('://')
			#print resource
			resource = self.parsed['identifier'].get(resource[1],False)
			#print resource
			if resource:
				noticeIcon = resource['Data']
				
		
		growl.notify(
			noteType = self.parsed['Notification-Name'],
			title = self.parsed['Notification-Title'],
			description=self.parsed['Notification-Text'],
			icon=noticeIcon
		)
			
	def __unicode__(self):
		return self.parsed