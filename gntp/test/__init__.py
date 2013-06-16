# Copyright: 2013 Paul Traylor
# These sources are released under the terms of the MIT license: see LICENSE

import unittest
from gntp.config import GrowlNotifier


class GNTPTestCase(unittest.TestCase):
	application = 'GNTP unittest'
	notification_name = 'Testing'

	notification = {
		'noteType': notification_name,
		'title': 'Unittest Title',
		'description': 'Unittest Description',
	}

	def setUp(self):
		self.growl = GrowlNotifier(self.application, [self.notification_name])
		self.growl.register()

	def _notify(self, **kargs):
		for k in self.notification:
			if not k in kargs:
				kargs[k] = self.notification[k]

		return self.growl.notify(**kargs)

	def assertIsTrue(self, result):
		"""Python 2.5 safe way to assert that the result is true"""
		return self.assertEqual(result, True)
