#!/usr/bin/env python

from gntp import __version__ as gntpversion
from distutils.core import setup
setup(
	name='gntp',
	description='Growl Notification Transport Protocol for Python',
	author='Paul Traylor',
	url='http://github.com/kfdm/gntp/',
	version=gntpversion,
	packages=['gntp'],
	# http://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
	],
	)