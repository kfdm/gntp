#!/usr/bin/env python
# Test the various hashing methods
import unittest
import logging
logging.basicConfig(level=logging.WARNING)
from gntp.notifier import GrowlNotifier


class Growler(GrowlNotifier):
	def hash_test(self, hashName):
		self.passwordHash = hashName
		return self.notify('Testing', 'Testing Hash', hashName)


class TestHash(unittest.TestCase):
	def setUp(self):
		self.growl = Growler('GNTP unittest', ['Testing'])
		self.growl.register()

	def test_md5(self):
		self.assertTrue(self.growl.hash_test('MD5'))

	def test_sha1(self):
		self.assertTrue(self.growl.hash_test('SHA1'))

	def test_sha256(self):
		self.assertTrue(self.growl.hash_test('SHA256'))

	def test_sha512(self):
		self.assertTrue(self.growl.hash_test('512'))

	def test_fake(self):
		'''Fake hash should not work'''
		self.assertFalse(self.growl.hash_test('fake-hash'))

if __name__ == '__main__':
	unittest.main()
