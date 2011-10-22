#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple test to send each priority level
import unittest
import logging
logging.basicConfig(level=logging.WARNING)
from gntp.notifier import GrowlNotifier


class TestHash(unittest.TestCase):
    def setUp(self):
        self.growl = GrowlNotifier('GNTP unittest', ['Testing'])
        self.growl.register()

    def test_lines(self):
        for priority in [2, 1, 0, -1, -2]:
            msg = 'Priority %s' % priority
            self.growl.notify('Testing', msg, msg, priority=priority)

if __name__ == '__main__':
    unittest.main()
