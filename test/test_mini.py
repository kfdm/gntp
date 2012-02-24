#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test most basic GNTP functions using our mini growl function
"""

import unittest
import logging
logging.basicConfig(level=logging.WARNING)
import gntp.config
import gntp.notifier

APPLICATION_NAME = "GNTP unittest"
ICON_URL = "https://www.google.com/intl/en_com/images/srpr/logo3w.png"
ICON_FILE = "test/growl-icon.png"
CALLBACK_URL = "http://github.com"


class TestHash(unittest.TestCase):
	def test_mini(self):
		gntp.notifier.mini('Testing gntp.notifier.mini',
			applicationName=APPLICATION_NAME
			)

	def test_config(self):
		gntp.config.mini('Testing gntp.config.mini',
			applicationName=APPLICATION_NAME
			)

	def test_url_icon(self):
		gntp.config.mini('Testing URL icon',
			applicationName=APPLICATION_NAME,
			applicationIcon=ICON_URL
			)

	def test_file_icon(self):
		gntp.notifier.mini('Testing URL icon',
			applicationName=APPLICATION_NAME,
			applicationIcon=open(ICON_FILE).read()
			)

	def test_sticky(self):
		gntp.config.mini('Testing sticky',
			applicationName=APPLICATION_NAME,
			sticky=True
			)

	def test_callback(self):
		gntp.config.mini('Testing Callback',
			applicationName=APPLICATION_NAME,
			callback=CALLBACK_URL
			)

if __name__ == '__main__':
	unittest.main()
