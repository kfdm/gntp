#!/usr/bin/env python
import sys
sys.path = ['..'] + sys.path
import gntp.notifier

class TestNotifier(gntp.notifier.GrowlNotifier):
	hostname = 'shiroi'
	password = 'testpassword'
	notifications = ['Test']
	debug = True

growl = TestNotifier()
growl.register()

for hash in ['MD5','SHA1','SHA256','SHA512']:
	growl.passwordHash = hash
	growl.notify('Test','Test Hash',hash)
