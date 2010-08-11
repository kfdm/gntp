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

gntp/config.py
--------------
This is a class that is used mostly with the `client.py` and `server.p`y examples
to hold some of the default values that I use mostly in testing

client.py
---------
Test client that shows the basic options.  Attempts to mimic some of the
[growlnotify](http://growl.info/extras.php#growlnotify) flags

server.py
---------
This is a test server that I use on my local machine for listening to gntp
messages

gntp_notifier.py
----------------
This is the bit of glue code used to 'regrowl' a gntp message to the native
[OSX Growl](http://growl.info/)
