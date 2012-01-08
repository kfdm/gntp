.. toctree::
	:maxdepth: 2
	:hidden:
	
	core

GNTP Basics
===========

Python bindings for the
`Growl Notification Transport Protocol <http://www.growlforwindows.com/gfw/help/gntp.aspx>`_

Bugs can be reported at the `GitHub issue tracker <https://github.com/kfdm/gntp/issues>`_

Sending a message
-----------------

.. automodule:: gntp.notifier
	:members:

Example Usage
-------------
::

	import gntp.notifier

	# Simple "fire and forget" notification
	gntp.notifier.mini("Here's a quick message")

	# More complete example
	growl = gntp.notifier.GrowlNotifier(
		applicationName = "My Application Name",
		notifications = ["New Updates","New Messages"],
		defaultNotifications = ["New Messages"],
		# hostname = "computer.example.com", # Defaults to localhost
		# password = "abc123" # Defaults to a blank password
	)
	growl.register()

	# Send one message
	growl.notify(
		noteType = "New Messages",
		title = "You have a new message",
		description = "A longer message description",
		icon = "http://example.com/icon.png",
		sticky = False,
		priority = 1,
	)

	# Try to send a different type of message
	# This one may fail since it is not in our list
	# of defaultNotifications
	growl.notify(
		noteType = "New Updates",
		title = "There is a new update to download",
		description = "A longer message description",
		icon = "http://example.com/icon.png",
		sticky = False,
		priority = -1,
	)