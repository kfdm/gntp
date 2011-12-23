# GNTP

This is a Python library for working with the [Growl Notification Transport Protocol](http://www.growlforwindows.com/gfw/help/gntp.aspx)

It should work as a dropin replacement for the older Python bindings


## Installation
You can install with pip

	$ pip install gntp

then test the module

	$ python -m gntp.notifier

## Simple Usage

```python
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

# Send a different message
growl.notify(
	noteType = "New Updates",
	title = "There is a new update to download",
	description = "A longer message description",
	icon = "http://example.com/icon.png",
	sticky = False,
	priority = -1,
)

```

## Bugs

[GitHub issue tracker](https://github.com/kfdm/gntp/issues)
