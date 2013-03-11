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

.. autoclass:: gntp.core.GNTPRegister
	:members:
	:inherited-members:

.. autoclass:: gntp.core.GNTPNotice
	:members:
	:inherited-members:

.. autoclass:: gntp.core.GNTPSubscribe
	:members:
	:inherited-members:

.. autoclass:: gntp.core.GNTPOK
	:members:
	:inherited-members:

.. autoclass:: gntp.core.GNTPError
	:members:
	:inherited-members:


Helper Functions
----------------

.. autofunction:: gntp.core.parse_gntp
