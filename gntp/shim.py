import sys

PY3 = sys.version_info[0] == 3

if PY3:
	def b(s):
		if isinstance(s, bytes):
			return s
		return s.encode('utf8', 'replace')

	def u(s):
		if isinstance(s, bytes):
			return s.decode('utf8', 'replace')
		return s

	import io
	StringIO = io.StringIO
	BytesIO = io.BytesIO
	from configparser import RawConfigParser
else:
	def b(s):
		if isinstance(s, unicode):
			return s.encode('utf8', 'replace')
		return s

	def u(s):
		if isinstance(s, unicode):
			return s
		if isinstance(s, int):
			s = str(s)
		return unicode(s, "utf8", "replace")

	int2byte = chr
	import StringIO
	StringIO = BytesIO = StringIO.StringIO
	from ConfigParser import RawConfigParser
