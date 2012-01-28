#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

import gntp

setup(
	name='gntp',
	description='Growl Notification Transport Protocol for Python',
	author='Paul Traylor',
	url='http://github.com/kfdm/gntp/',
	version=gntp.__version__,
	packages=['gntp'],
	# http://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Operating System :: OS Independent',
	],
	entry_points={
		'console_scripts': [
			'gntp = gntp.cli:main'
		]
	}
)
