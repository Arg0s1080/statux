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

from time import strftime, localtime
from datetime import timedelta
from platform import machine

_PARENT = "/proc/"
_STAT = "%sstat" % _PARENT
_UPTIME = "%suptime" % _PARENT
_INIT = "%s1/comm" % _PARENT
_INFO_KERNEL = "%ssys/kernel/" % _PARENT


def boot_time(str_format=False):
    """Returns the time at which the system booted

        :Params:
            str_format (bool): If is False returns seconds since the Unix epoch (January 1, 1970),
                               if is set to True returns a formatted string with the system boot
                               time. False by default.
    """
    def sformat(v):
        return strftime('%Y-%m-%d %H:%M:%S', localtime(v))

    with open(_STAT, "rb") as f:
        for line in f.readlines():
            if line.startswith(b"btime"):
                r = int(line.split()[1])
                return r if not str_format else sformat(r)


def uptime(str_format=False):
    """Returns the time elapsed since system boot time

        :Params:
            :str_format (bool): If is set to True returns a formatted string, seconds otherwise.
                                False by default
    """
    with open(_UPTIME, "rb") as f:
        sec = float(f.readline().split()[0])
        return str(timedelta(seconds=sec)).rstrip("0").rstrip(".") if str_format else sec


def init() -> str:
    """Returns init system name (e.g.: systemd, sysvinit, upstart, etc)"""
    with open(_INIT, "r") as f:
        return f.read()[:-1]


def hostname() -> str:
    """Returns hostname"""
    with open("%shostname" % _INFO_KERNEL, "r") as f:
        return f.read()[:-1]


def kernel_release():
    """Returns kernel release (e.g.: '#25-Ubuntu SMP Wed May 23 18:02:16 UTC 2018')"""
    with open("%sosrelease" % _INFO_KERNEL, "r") as f:
        return f.read()[:-1]


def kernel_version():
    """Returns kernel version (e.g.: '4.15.0-23-generic')"""
    with open("%sversion" % _INFO_KERNEL, "r") as f:
        return f.read()[:-1]


def architecture():
    """Returns the machine type, (e.g.: 'x86_64' or 'i386')"""
    return machine()
