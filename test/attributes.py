#!/usr/bin/env python
# Simple manual test to make sure that attributes do not
# accumulate in the base classes
# https://github.com/kfdm/gntp/issues/10

import gntp
import gntp.notifier

a = gntp.notifier.GrowlNotifier(notifications=['A'])
b = gntp.notifier.GrowlNotifier(notifications=['B'])

a.notify('A','A','A',sticky=True)
b.notify('B','B','B')
