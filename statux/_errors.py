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
# (ɔ) Iván Rincón 2019

import errno
from sys import platform
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
        #super(ValueNotFoundError, self).__init__(self.value, self.filename, self.strerror)
        super(OSError, self).__init__(self.errno, self.strerror, self.filename)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.args)


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

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.args)


class UnexpectedValueError(ValueError, StatuxError):
    def __init__(self, msg, cause, expected=None):
        self.cause = cause
        self.msg = msg
        self.expected = expected
        self.args = (self.msg, self.cause, self.expected)
        super(ValueError, self).__init__(self.msg, self.cause, self.expected)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.args)


class TempNotFoundError(StatuxError):
    def __init__(self, value, msg=""):
        self.value = value
        self.strerror = msg or ("%s value not found" % self.value)
        self.args = (self.strerror, self.value)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.args)


class PlatformError(RuntimeError, StatuxError):
    def __init__(self, os):
        self.platform = os
        self.strerror = "'%s' platform is not supported. Statux only works on Linux" % os.title()
        self.args = (self.strerror, self.platform)
        super(RuntimeError, self).__init__(self.strerror, self.platform)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.args)


class PartitionNotMountError(StatuxError):
    def __init__(self, partition):
        self.partition = partition
        self.strerror = "%s is not mount" % self.partition
        self.args = self.strerror, self.partition
        super(PartitionNotMountError, self).__init__(self.partition)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.args)


class UnsupportedScaleError(ValueError, StatuxError):
    def __init__(self, scale):
        self.scale = scale
        self.strerror = "Unsupported scale"
        self.args = self.scale, self.strerror
        super(ValueError, self).__init__(self.strerror, self.scale)

    def __repr__(self):
        return "%s%s%s" % (self.__class__.__name__, self.strerror, self.args)


def ex_handler(filename, value=""):
    def raiser(fun):
        def wrapper(*args, **kwargs):
            def get_name():
                # Returns method name
                return fun.__name__.replace("_", " ")
            try:
                return fun(*args, **kwargs)
            except UnexpectedValueError:
                raise
            except FileNotFoundError:
                raise ValueNotFoundError(value or get_name(), filename, errno.ENOENT, msg=strerror(errno.ENOENT))
            except ValueError as ex:
                msg = "%s: %s" % (strerror(errno.ENOMSG), ex.args[0])
                raise ValueNotFoundError(value or get_name(), filename, errno.ENOMSG, msg=msg)
        return wrapper
    return raiser


if not platform.lower().startswith("linux"):
    raise PlatformError(platform)

# from sys import version_info
# if not version_info.major == 3:
#     print("Python 3 is needed")
#     exit(1)
