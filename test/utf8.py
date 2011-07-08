# -*- coding: utf-8 -*-
# Simple script to test sending UTF8 text with the GrowlNotifier class
import logging
logging.basicConfig(level=logging.INFO)
from gntp.notifier import GrowlNotifier

growl = GrowlNotifier(notifications=['Testing'],hostname='ayu')
growl.register()
growl.notify('Testing','Testing','Hello')
growl.notify('Testing','Testing','allô')
growl.notify('Testing','Testing',u'おはおう')
