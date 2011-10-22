#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple script to test sending UTF8 text with the GrowlNotifier class
import unittest
import logging
logging.basicConfig(level=logging.WARNING)
from gntp.notifier import GrowlNotifier


class TestHash(unittest.TestCase):
	def setUp(self):
		self.growl = GrowlNotifier('GNTP unittest', ['Testing'])
		self.growl.register()
	def test_english(self):
		self.growl.notify('Testing','Testing','Hello')
	def test_extra(self):
		self.growl.notify('Testing','Testing','allô')
	def test_japanese(self):
		self.growl.notify('Testing','Testing',u'おはおう')

if __name__ == '__main__':
	unittest.main()
