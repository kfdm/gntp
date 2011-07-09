# Test the various hashing methods
import logging
logging.basicConfig(level=logging.DEBUG)
from gntp.notifier import GrowlNotifier

growl = GrowlNotifier(notifications=['Testing'],password='password',hostname='ayu')
growl.register()

for hash in ['MD5','SHA1','SHA256','SHA512','fake-hash']:
	print '-'*80
	print 'Testing',hash
	print '-'*80
	growl.passwordHash = hash
	growl.notify('Testing','Test Hash',hash)
