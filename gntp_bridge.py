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
	
	appIcon = self.headers.get('Application-Icon',None)
	if appIcon:
		resource = appIcon.split('://')
		appIcon = self.resources.get(resource[1])['Data']
	
	growl = Growl.GrowlNotifier(
		applicationName			= self.headers['Application-Name'],
		notifications			= notifications,
		defaultNotifications	= defaultNotifications,
		applicationIcon			= appIcon,
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
	
	noticeIcon = self.headers.get('Notification-Icon',None)
	if noticeIcon:
		resource = noticeIcon.split('://')
		noticeIcon = self.resources.get(resource[1])['Data']
	
	growl.notify(
		noteType = self.headers['Notification-Name'],
		title = self.headers['Notification-Title'],
		description=self.headers.get('Notification-Text',''),
		icon=noticeIcon
	)
	return self.encode()

GNTPRegister.send = register_send
GNTPNotice.send = notice_send
