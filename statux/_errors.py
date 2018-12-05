#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
#
# Permissions of this strong copyleft license are conditioned on making available
# complete source code of licensed works and modifications, which include larger works
# using a licensed work, under the same license. Copyright and license notices must be
# preserved. Contributors provide an express grant of patent rights.
#
# For more information on this, and how to apply and follow theGNU GPL, see:
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018

import errno
from os import strerror
from os.path import basename

# errno.ENOENT  = 2   # No such file or directory
# errno.ENODEV  = 19  # No such device
# errno.EROFS   = 30  # Read-only file system
# errno.ENODATA = 61  # No data available
# errno.ENOMSG  = 42  # No message of desired type


class StatuxError(Exception):
    pass


class ValueNotFoundError(OSError, StatuxError):
    def __init__(self, value, filename, err_no, msg=""):
        self.errno = err_no
        self.value = value
        self.filename = filename
        self.strerror = msg or ("%s: %s not found in %s" %
                                (strerror(self.errno), self.value, basename(self.filename)))
        self.args = (self.errno, self.strerror, self.filename, self.value)
        super(OSError, self).__init__(self.errno, self.strerror, self.filename)

    def __repr__(self):
        return str(self.args)


class DeviceNotFoundError(ValueNotFoundError):
    def __init__(self, value, filename, device, msg="", err_no=errno.ENODEV):
        self.errno = err_no
        self.value = value
        self.filename = filename
        self.device = device
        self.strerror = msg or ("%s: %s not found. Search for %s in %s" %
                                (strerror(self.errno), self.device, self.value, basename(self.filename)))
        self.args = (self.errno, self.strerror, self.filename, self.value, self.device)
        super(ValueNotFoundError, self).__init__(self.value, self.filename, self.errno, msg)


class UnexpectedValueError(ValueError, StatuxError):
    def __init__(self, msg, cause, expected=None):
        self.cause = cause
        self.msg = msg
        self.expected = expected
        self.args = (self.msg, self.cause, self.expected)
        super(ValueError, self).__init__(self.msg, self.cause, self.expected)

    def __repr__(self):
        return str(self.args)


def cpu_ex_handler(filename, value=""):
    def raiser(fun):
        def wrapper(*args, **kwargs):
            def get_value():
                return fun.__name__.replace("_", " ")
            try:
                return fun(*args, **kwargs)
            except UnexpectedValueError:
                raise
            except FileNotFoundError:
                raise ValueNotFoundError(value or get_value(), filename, errno.ENOENT, msg=strerror(errno.ENOENT))
            except ValueError as ex:
                msg = "%s: %s" % (strerror(errno.ENOMSG), ex.args[0])
                raise ValueNotFoundError(value or get_value(), filename, errno.ENOMSG, msg=msg)
        return wrapper
    return raiser
