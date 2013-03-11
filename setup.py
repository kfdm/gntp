try:
	from setuptools import setup
	kwargs = {
		'entry_points':{
			'console_scripts': [
				'gntp = gntp.cli:main'
			]
		}
	}
except ImportError:
	from distutils.core import setup
	kwargs = {
		'scripts':['scripts/gntp']
	}

from gntp.version import __version__

setup(
	name='gntp',
	description='Growl Notification Transport Protocol for Python',
	long_description=open('README.rst').read(),
	author='Paul Traylor',
	url='http://github.com/kfdm/gntp/',
	version=__version__,
	packages=['gntp'],
	# http://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.5',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: Implementation :: PyPy',
	],
	**kwargs
)
