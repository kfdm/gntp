#!/usr/bin/env python
import sys
sys.path = ['..'] + sys.path
import gntp.notifier
import platform

class TestNotifier(gntp.notifier.GrowlNotifier):
	hostname = 'shiroi'
	password = 'testpassword'
	notifications = ['Test']
	debug = True

growl = TestNotifier()
growl.subscribe(platform.node(),platform.node(),12345)
