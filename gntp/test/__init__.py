import unittest
from gntp.config import GrowlNotifier


class GNTPTestCase(unittest.TestCase):
	notification = {
		'noteType': 'Testing',
		'title': 'Unittest Title',
		'description': 'Unittest Description',
	}

	def setUp(self):
		self.growl = GrowlNotifier('GNTP unittest', ['Testing'])
		self.growl.register()

	def _notify(self, **kargs):
		for k in self.notification:
			if not k in kargs:
				kargs[k] = self.notification[k]

		return self.growl.notify(**kargs)
