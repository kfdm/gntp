"""
Test sending custom attributes

http://www.growlforwindows.com/gfw/help/gntp.aspx#custom
"""

from gntp.test import GNTPTestCase


class TestCustom(GNTPTestCase):
	def test_custom_values(self):
		self._notify(title='Custom Attributes', custom={
				'X-Custom1': 'Some Value',
				'X-Custom2': 'Some other value',
			})
