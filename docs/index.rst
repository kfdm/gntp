.. toctree::
	:maxdepth: 2
	:hidden:
	
	core

GNTP Basics
===========

Python bindings for the
`Growl Notification Transport Protocol <http://www.growlforwindows.com/gfw/help/gntp.aspx>`_

Bugs can be reported at the `GitHub issue tracker <https://github.com/kfdm/gntp/issues>`_

Simple Message Sending
----------------------

::

	from gntp.notifier import mini
	# Send a simple growl message with mostly default values
	mini("Here's a quick message", callback="http://github.com/")

.. autofunction:: gntp.notifier.mini


Detailed Message Sending
------------------------

.. autoclass:: gntp.notifier.GrowlNotifier

The GrowlNotifier class is intended to mostly mirror the older python bindings
for growl

.. automethod:: gntp.notifier.GrowlNotifier.register

.. automethod:: gntp.notifier.GrowlNotifier.notify

.. automethod:: gntp.notifier.GrowlNotifier.subscribe



Complete Example
----------------
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

	# Send the image with the growl notification
	image = open('/path/to/icon.png', 'rb').read()
	growl.notify(
		noteType = "New Messages",
		title = "Now with icons",
		description = "This time we attach the image",
		icon = image,
	)

GNTP Configfile Example
-----------------------
.. autoclass:: gntp.config.GrowlNotifier
