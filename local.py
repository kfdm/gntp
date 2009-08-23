import gntp
import Growl

GNTPParseError = gntp.GNTPParseError
GNTPOK = gntp.GNTPOK
GNTPError = gntp.GNTPError
parse_gntp = gntp.parse_gntp

class GNTPRegister(gntp.GNTPRegister):
	def send(self):
		print 'Sending Local Registration'
		
		#Local growls only need a list of strings
		notifications=[]
		defaultNotifications = []
		for notice in self.notifications:
			notifications.append(notice['Notification-Name'])
			if notice.get('Notification-Enabled',True):
				defaultNotifications.append(notice['Notification-Name'])
				
		growl = Growl.GrowlNotifier(
			applicationName			= self.headers['Application-Name'],
			notifications			= notifications,
			defaultNotifications	= defaultNotifications,
		)
		growl.register()
		
class GNTPNotice(gntp.GNTPNotice):
	def send(self):
		print 'Sending Local Notification'
		growl = Growl.GrowlNotifier(
			applicationName			= self.headers['Application-Name'],
			notifications			= [self.headers['Notification-Name']]
		)
		
		noticeIcon = None
		if self.headers.get('Notification-Icon',False):
			resource = self.headers['Notification-Icon'].split('://')
			#print resource
			resource = self.resources.get(resource[1],False)
			#print resource
			if resource:
				noticeIcon = resource['Data']
		
		growl.notify(
			noteType = self.headers['Notification-Name'],
			title = self.headers['Notification-Title'],
			description=self.headers['Notification-Text'],
		)