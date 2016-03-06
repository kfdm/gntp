# -*- coding: utf-8 -*-
# Copyright: 2013 Paul Traylor
# These sources are released under the terms of the MIT license: see LICENSE

# Simple test to send each priority level
import logging
logging.basicConfig(level=logging.WARNING)

import os
import unittest

from gntp.test import GNTPTestCase
import gntp.config
import gntp.core
import gntp.errors as errors
import gntp.notifier

ICON_URL = "https://www.google.com/intl/en_com/images/srpr/logo3w.png"
ICON_FILE = os.path.join(os.path.dirname(__file__), "growl-icon.png")
CALLBACK_URL = "http://github.com"


class BasicTests(GNTPTestCase):
	def test_mini(self):
		gntp.notifier.mini('Testing gntp.notifier.mini',
			applicationName=self.application
			)

	def test_config(self):
		gntp.config.mini('Testing gntp.config.mini',
			applicationName=self.application
			)

	def test_priority(self):
		for priority in [2, 1, 0, -1, -2]:
			self.assertIsTrue(self._notify(
				description='Priority %s' % priority,
				priority=priority
				))

	def test_english(self):
		self.assertIsTrue(self._notify(description='Hello World'))

	def test_extra(self):
		self.assertIsTrue(self._notify(description='allô'))

	def test_japanese(self):
		self.assertIsTrue(self._notify(description='おはおう'))

	def test_sticky(self):
		self.assertIsTrue(self._notify(sticky=True, description='Sticky Test'))

	def test_unknown_note(self):
		self.assertRaises(AssertionError, self._notify, noteType='Unknown')

	def test_parse_error(self):
		self.assertRaises(errors.ParseError, gntp.core.parse_gntp, 'Invalid GNTP Packet')

	def test_url_icon(self):
		self.assertIsTrue(self._notify(
			icon=ICON_URL,
			description='test_url_icon',
			))

	def test_data_icon(self):
		self.assertIsTrue(self._notify(
			icon=open(ICON_FILE, 'rb').read(),
			description='test_data_icon',
			))

	def test_file_icon(self):
		self.assertIsTrue(self._notify(
			icon='file://' + os.path.abspath(ICON_FILE),
			description='test_file_icon',
		))

	def test_callback(self):
		self.assertIsTrue(self._notify(
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
