.. GNTP documentation master file, created by
   sphinx-quickstart on Tue Aug 30 22:54:03 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GNTP's documentation!
================================

Python bindings for the
`Growl Notification Transport Protocol <http://www.growlforwindows.com/gfw/help/gntp.aspx>`_



.. toctree::
   :maxdepth: 2

Sending GNTP Messages
---------------------

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