Core GNTP Classes
=================
Lower level classes for those who want more control in sending messages

Exceptions
----------

.. autoexception:: gntp.errors.AuthError

.. autoexception:: gntp.errors.ParseError

.. autoexception:: gntp.errors.UnsupportedError

GNTP Messages
-------------
Classes representing each of the GNTP message types

.. autoclass:: gntp.GNTPRegister
	:members:
	:inherited-members:

.. autoclass:: gntp.GNTPNotice
	:members:
	:inherited-members:

.. autoclass:: gntp.GNTPSubscribe
	:members:
	:inherited-members:

.. autoclass:: gntp.GNTPOK
	:members:
	:inherited-members:

.. autoclass:: gntp.GNTPError
	:members:
	:inherited-members:


Helper Functions
----------------

.. autofunction:: gntp.parse_gntp