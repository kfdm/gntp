# GNTP

This is a Python library for working with the [Growl Notification Transport Protocol](http://www.growlforwindows.com/gfw/help/gntp.aspx)

It should work as a dropin replacement for the older Python bindings

## Simple Usage

```python
import gntp.notifier
growl = gntp.notifier.GrowlNotifier(
	applicationName = "My Application Name",
	notifications = ["New Updates","New Message"],
	defaultNotifications = ["New Messages"],
	hostname = "computer.example.com",
	password = "abc123"
)
growl.register()

growl.notify(
	noteType = "New Message",
	title = "You have a new message",
	description = "A longer message description",
	icon = "http://example.com/icon.png",
	sticky = False,
	priority = 1,
)
```

## Installation

	$ pip install gntp

## Bugs

[GitHub issue tracker](https://github.com/kfdm/gntp/issues)
