from gntp import *
import Growl

def register_send(self):
	'''
	Resend a GNTP Register message to Growl running on a local OSX Machine
	'''
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
	return self.encode()
	
def notice_send(self):
	'''
	Resend a GNTP Notify message to Growl running on a local OSX Machine
	'''
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
		description=self.headers.get('Notification-Text',''),
	)
	return self.encode()

GNTPRegister.send = register_send
GNTPNotice.send = notice_send