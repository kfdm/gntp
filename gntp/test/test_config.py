# Copyright: 2013 Paul Traylor
# These sources are released under the terms of the MIT license: see LICENSE

# Test when we don't have a config file
# Since we don't know if the user will have a config file or not when
# running this test, we will move it out of the way and then move it back
# when we're done

import os
from gntp.test import GNTPTestCase
from gntp.config import GrowlNotifier

ORIGINAL_CONFIG = os.path.expanduser('~/.gntp')
BACKUP_CONFIG = os.path.expanduser('~/.gntp.backup')


class ConfigTests(GNTPTestCase):
	def setUp(self):
		if os.path.exists(ORIGINAL_CONFIG):
			os.rename(ORIGINAL_CONFIG, BACKUP_CONFIG)
		self.growl = GrowlNotifier(self.application, [self.notification_name])
		self.growl.register()

	def test_missing_config(self):
		self.assertIsTrue(self._notify(description='No config file test'))

	def tearDown(self):
		if os.path.exists(BACKUP_CONFIG):
			os.rename(BACKUP_CONFIG, ORIGINAL_CONFIG)
