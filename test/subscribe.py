# -*- coding: utf-8 -*-
# Simple script to test sending UTF8 text with the GrowlNotifier class
import logging
logging.basicConfig(level=logging.DEBUG)
from gntp.notifier import GrowlNotifier
import platform

growl = GrowlNotifier(notifications=['Testing'],password='password',hostname='ayu')
growl.subscribe(platform.node(),platform.node(),12345)
