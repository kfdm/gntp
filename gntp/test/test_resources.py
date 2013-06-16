# Copyright: 2013 Paul Traylor
# These sources are released under the terms of the MIT license: see LICENSE

# https://github.com/kfdm/gntp/issues/27
# nosetests -v gntp.test.test_resources:ResourceTest

import os

from gntp.test import GNTPTestCase
import gntp.core

ICON_FILE = os.path.join(os.path.dirname(__file__), "growl-icon.png")
ICON_DATA = open(ICON_FILE, 'rb').read()
FILE_DATA = open(__file__).read()


class ResourceTest(GNTPTestCase):
	def test_single_resource(self):
		notification = gntp.core.GNTPNotice(
			app=self.application,
			name=self.notification_name,
			title="Testing Single Resource",
			password=self.growl.password,
			)
		resource = notification.add_resource(ICON_DATA)
		notification.add_header('Notification-Icon', resource)
		self.assertIsTrue(self.growl._send('notify', notification))

	def test_double_resource(self):
		notification = gntp.core.GNTPNotice(
			app=self.application,
			name=self.notification_name,
			title="Testing Double Resource",
			password=self.growl.password,
			)

		notification.add_resource(FILE_DATA)
		resource = notification.add_resource(ICON_DATA)
		notification.add_header('Notification-Icon', resource)

		self.assertIsTrue(self.growl._send('notify', notification))
