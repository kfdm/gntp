#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple test to send each priority level
import logging
logging.basicConfig(level=logging.WARNING)

import os
import unittest
from gntp.test import GNTPTestCase
import gntp
import gntp.config
import gntp.notifier

APPLICATION_NAME = "GNTP unittest"
ICON_URL = "https://www.google.com/intl/en_com/images/srpr/logo3w.png"
ICON_FILE = os.path.join(os.path.dirname(__file__), "growl-icon.png")
CALLBACK_URL = "http://github.com"


class BasicTests(GNTPTestCase):
	def test_mini(self):
		gntp.notifier.mini('Testing gntp.notifier.mini',
			applicationName=APPLICATION_NAME
			)

	def test_config(self):
		gntp.config.mini('Testing gntp.config.mini',
			applicationName=APPLICATION_NAME
			)

	def test_priority(self):
		for priority in [2, 1, 0, -1, -2]:
			self.assertTrue(self._notify(
				description='Priority %s' % priority,
				priority=priority
				))

	def test_english(self):
		self.assertTrue(self._notify(description='Hello World'))

	def test_extra(self):
		self.assertTrue(self._notify(description='allô'))

	def test_japanese(self):
		self.assertTrue(self._notify(description='おはおう'))

	def test_sticky(self):
		self.assertTrue(self._notify(sticky=True, description='Sticky Test'))

	def test_unknown_note(self):
		self.assertRaises(AssertionError, self._notify, noteType='Unknown')

	def test_parse_error(self):
		self.assertRaises(gntp.ParseError, gntp.parse_gntp, 'Invalid GNTP Packet')

	def test_url_icon(self):
		self.assertTrue(self._notify(
			icon=ICON_URL,
			description='test_url_icon',
			))

	def test_file_icon(self):
		self.assertTrue(self._notify(
			icon=open(ICON_FILE).read(),
			description='test_file_icon',
			))

	def test_callback(self):
		self.assertTrue(self._notify(
			callback=CALLBACK_URL,
			description='Testing Callback',
			))

	#def test_subscribe(self):
	#	self.assertTrue(self.growl.subscribe(
	#		id='unittest-id',
	#		name='example.com',
	#		port=5000,
	#		))

if __name__ == '__main__':
	unittest.main()
