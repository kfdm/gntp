# Copyright: 2013 Paul Traylor
# These sources are released under the terms of the MIT license: see LICENSE

"""
Test the various error condtions

This test runs with the gntp.config module so that we can
get away without having to hardcode our password in a test
script. Please fill out your ~/.gntp config before running
"""

from gntp.test import GNTPTestCase
import gntp.errors as errors


class TestErrors(GNTPTestCase):
	def test_connection_error(self):
		#self.growl.hostname = '0.0.0.0'
		# Port 9 would be the  discard protocol. We just want a "null port"
		# for testing
		# http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
		self.growl.port = 9
		self.assertRaises(errors.NetworkError, self._notify, description='Connection Error')
