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
from os.path import basename

# errno.ENOENT  = 2   # No such file or directory
# errno.ENODEV  = 19  # No such device
# errno.EROFS   = 30  # Read-only file system
# errno.ENODATA = 61  # No data available
# errno.ENOMSG  = 42  # No message of desired type


class StatuxError(OSError):
    pass


class ValueNotFoundError(StatuxError):
    def __init__(self, value, filename, err_no=errno.ENOENT, msg=""):
        self.errno = err_no
        self.value = value
        self.filename = filename
        self.strerror = msg or "%s not found in %s" % (self.value, basename(self.filename))
        self.args = (self.errno, self.strerror, self.filename)
        super(StatuxError, self).__init__(self.errno, self.strerror, self.filename)

    def __repr__(self):
        return str(self.args)
