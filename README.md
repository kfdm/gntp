Python library for working with Growl Notification Transport Protocol (GNTP)
============================================================================

gntp/__init__.py
----------------
This contains the core of the GNTP code.  It can be imported using

    import gntp

gntp/notifier.py
----------------
This class uses a similar interface to the official python bindings that come
with the [Growl SDK](http://code.google.com/p/growl/source/browse/Bindings/python/Growl.py)

client.py
---------
Test client that shows the basic options.  Attempts to mimic some of the
[growlnotify](http://growl.info/extras.php#growlnotify) flags
