try:
	from ConfigParser import RawConfigParser
except ImportError:
	from configparser import RawConfigParser

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO
