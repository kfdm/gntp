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
	growl = gntp.notifier.GrowlNotifier(
		applicationName = "My Application Name",
		notifications = ["New Updates","New Messages"],
		defaultNotifications = ["New Messages"],
		hostname = "computer.example.com",
		password = "abc123"
	)
	growl.register()
	
	result = growl.notify(
		noteType = "New Message",
		title = "You have a new message",
		description = "A longer message description",
		icon = "http://example.com/icon.png",
		sticky = False,
		priority = 1,
	)