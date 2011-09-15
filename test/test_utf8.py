#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple script to test sending UTF8 text with the GrowlNotifier class
import unittest
import logging
logging.basicConfig(level=logging.WARNING)
import gntp.notifier

class Growler(gntp.notifier.GrowlNotifier):
	applicationName = 'GNTP unittest'
	hostname = 'localhost'
	port = 23053
	notifications=['Testing']

class TestHash(unittest.TestCase):
	def setUp(self):
		self.growl = Growler()
		self.growl.register()
	def test_english(self):
		self.growl.notify('Testing','Testing','Hello')
	def test_extra(self):
		self.growl.notify('Testing','Testing','allô')
	def test_japanese(self):
		self.growl.notify('Testing','Testing',u'おはおう')

if __name__ == '__main__':
	unittest.main()
