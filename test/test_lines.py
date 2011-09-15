#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple script to test sending UTF8 text with the GrowlNotifier class
import unittest
import os
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
		self.dir = os.path.dirname(__file__)
		self.file = os.path.join(self.dir,'test_lines.txt')
	def test_lines(self):
		for line in open(self.file):
			self.growl.notify('Testing','Line',line)

if __name__ == '__main__':
	unittest.main()
