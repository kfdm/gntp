import gntp
import Growl

class GNTPRegister(gntp.GNTPRegister):
	def send(self):
		print 'Sending Registration'
		growl = Growl.GrowlNotifier(
			applicationName			= self.headers['Application-Name'],
			notifications			= self.notifications,
			defaultNotifications	= self.defaultNotifications,
		)
		growl.register()
		
class GNTPNotice(gntp.GNTPNotice):
	def send(self):
		print 'Sending Notification'
		growl = Growl.GrowlNotifier(
			applicationName			= self.headers['Application-Name'],
			notifications			= [self.headers['Notification-Name']]
		)
		
		noticeIcon = None
		if self.headers.get('Notification-Icon',False):
			resource = self.headers['Notification-Icon'].split('://')
			#print resource
			resource = self.headers['identifier'].get(resource[1],False)
			#print resource
			if resource:
				noticeIcon = resource['Data']
		
		growl.notify(
			noteType = self.headers['Notification-Name'],
			title = self.headers['Notification-Title'],
			description=self.headers['Notification-Text'],
			icon=noticeIcon
		)