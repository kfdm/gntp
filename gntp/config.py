"""
The gntp.config module is provided as an extended GrowlNotifier object that takes
advantage of the ConfigParser module to allow us to setup some default values
(such as hostname, password, and port) in a more global way to be shared among
programs using gntp

Code duplication is bad, but for right now I have copied the mini() function
from the gntp.notifier class since I do not know of an easy way to reuse the
code yet fire using the copy of GrowlNotifier in this module
"""
import os
import ConfigParser
import gntp.notifier
import logging

__all__ = [
	'mini',
	'GrowlNotifier'
]

logger = logging.getLogger(__name__)


def mini(description, applicationName='PythonMini', noteType="Message",
			title="Mini Message", applicationIcon=None, hostname='localhost',
			password=None, port=23053, sticky=False, priority=None,
			callback=None, notificationIcon=None):
	"""Single notification function

	Simple notification function in one line. Has only one required parameter
	and attempts to use reasonable defaults for everything else
	:param string description: Notification message
	"""
	growl = GrowlNotifier(
		applicationName=applicationName,
		notifications=[noteType],
		defaultNotifications=[noteType],
		applicationIcon=applicationIcon,
		hostname=hostname,
		password=password,
		port=port,
	)
	result = growl.register()
	if result is not True:
		return result

	return growl.notify(
		noteType=noteType,
		title=title,
		description=description,
		icon=notificationIcon,
		sticky=sticky,
		priority=priority,
		callback=callback,
	)


class GrowlNotifier(gntp.notifier.GrowlNotifier):
	"""
	ConfigParser enhanced GrowlNotifier object

	For right now, we are only interested in letting users overide certain
	values from ~/.gntp

	::

		[gntp]
		hostname = ?
		password = ?
		port = ?
	"""
	def __init__(self, applicationName='Python GNTP', notifications=[],
			defaultNotifications=None, applicationIcon=None, hostname='localhost',
			password=None, port=23053):
		config = ConfigParser.RawConfigParser({
			'hostname': hostname,
			'password': password,
			'port': port,
		})

		config.read([os.path.expanduser('~/.gntp')])

		# If the file does not exist, then there will be no gntp section defined
		# and the config.get() lines below will get confused. Since we are not
		# saving the config, it should be safe to just add it here so the
		# code below doesn't complain
		if not config.has_section('gntp'):
			logger.warning('No [gntp] section found in ~/.gntp config file')
			config.add_section('gntp')

		self.applicationName = applicationName
		self.notifications = list(notifications)
		if defaultNotifications:
			self.defaultNotifications = list(defaultNotifications)
		else:
			self.defaultNotifications = self.notifications
		self.applicationIcon = applicationIcon

		self.password = config.get('gntp', 'password')
		self.hostname = config.get('gntp', 'hostname')
		self.port = config.getint('gntp', 'port')

if __name__ == '__main__':
	# If we're running this module directly we're likely running it as a test
	# so extra debugging is useful
	logging.basicConfig(level=logging.INFO)
	mini('Testing mini notification')
