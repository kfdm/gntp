#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple script to test sending UTF8 text with the GrowlNotifier class
import unittest
import os
import logging
logging.basicConfig(level=logging.WARNING)
from gntp.notifier import GrowlNotifier


class TestHash(unittest.TestCase):
	def setUp(self):
		self.growl = GrowlNotifier('GNTP unittest', ['Testing'])
		self.growl.register()
		self.dir = os.path.dirname(__file__)
		self.file = os.path.join(self.dir, 'test_lines.txt')

	def test_lines(self):
		for line in open(self.file):
			self.growl.notify('Testing', 'Line', line)

if __name__ == '__main__':
	unittest.main()
