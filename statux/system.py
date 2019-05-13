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
# For more information on this, and how to apply and follow the GNU GPL, see:
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2019

from statux._errors import ValueNotFoundError, StatuxError, ex_handler

_OS_RELEASE = "/etc/os-release"  # /usr/lib/os-release
_PROC_PTH = "/proc/"
_STAT = "%sstat" % _PROC_PTH
_UPTIME = "%suptime" % _PROC_PTH
_INIT = "%s1/comm" % _PROC_PTH
_INFO_KERNEL = "%ssys/kernel/" % _PROC_PTH
_HOSTNAME = "%shostname" % _INFO_KERNEL
_RELEASE = "%sosrelease" % _INFO_KERNEL
_VERSION = "%sversion" % _INFO_KERNEL
_SESSION_ID = "%sself/sessionid" % _PROC_PTH


def _get_os_release():
    def rpl(value):
        return value.replace('"', "").replace("'", '').replace("\n", "")
    with open(_OS_RELEASE, "r") as f:
        return {line.split("=")[0]: rpl(line.split("=")[1]) for line in f.readlines()}


@ex_handler(_STAT)
def boot_time(str_format=False, time_format="%Y-%m-%d %H:%M:%S"):
    """Returns the time at which the system booted

        :Params:
            str_format (bool): If is False returns seconds since the Unix epoch (January 1, 1970),
                               if is set to True returns a formatted string with the system boot
                               time. False by default.
            time_format (str): Time format using the C standard

                               Commonly used format codes:
                                %Y  Year with century as a decimal number.
                                %m  Month as a decimal number [01,12].
                                %d  Day of the month as a decimal number [01,31].
                                %H  Hour (24-hour clock) as a decimal number [00,23].
                                %M  Minute as a decimal number [00,59].
                                %S  Second as a decimal number [00,61].
                                %z  Time zone offset from UTC.
                                %a  Locale's abbreviated weekday name.
                                %A  Locale's full weekday name.
                                %b  Locale's abbreviated month name.
                                %B  Locale's full month name.
                                %c  Locale's appropriate date and time representation.
                                %I  Hour (12-hour clock) as a decimal number [01,12].
                                %p  Locale's equivalent of either AM or PM.

                                More info:
                                https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    from time import strftime, localtime
    with open(_STAT, "rb") as file:
        r = None
        for line in file:
            if line.startswith(b"btime"):
                r = int(line.split()[1])
                break
        return r if not str_format else strftime(time_format, localtime(r))


@ex_handler(_UPTIME)
def uptime(str_format=False):
    """Returns the time elapsed since system boot time

        :Params:
            :str_format (bool): If is set to True returns a formatted string, seconds otherwise.
                                False by default
    """
    from datetime import timedelta
    with open(_UPTIME, "rb") as f:
        sec = float(f.readline().split()[0])
        return str(timedelta(seconds=sec)).rstrip("0").rstrip(".") if str_format else sec


print(uptime(True))

@ex_handler(_INIT)
def init() -> str:
    """Returns init system name (e.g.: systemd, sysvinit, upstart, etc)"""
    with open(_INIT, "r") as f:
        return f.readline()[:-1]


@ex_handler(_HOSTNAME)
def hostname() -> str:
    """Returns hostname"""
    with open(_HOSTNAME, "r") as f:
        return f.readline()[:-1]


def user():
    """Returns current user"""
    from os import environ
    try:
        return environ["USER"]
    except KeyError:
        raise StatuxError("user name not found")


@ex_handler(_RELEASE)
def kernel_release() -> str:
    """Returns kernel release (e.g.: '#25-Ubuntu SMP Wed May 23 18:02:16 UTC 2018')"""
    with open(_RELEASE, "r") as f:
        return f.read()[:-1]


@ex_handler(_VERSION)
def kernel_version() -> str:
    """Returns kernel version (e.g.: '4.15.0-23-generic')"""
    with open(_VERSION, "r") as f:
        return f.read()[:-1]


def architecture() -> str:
    """Returns the machine type, (e.g.: 'x86_64' or 'i386')"""
    from platform import machine
    return machine()


@ex_handler(_SESSION_ID)
def session_id() -> int:
    """Returns current session id"""
    with open(_SESSION_ID, "rb") as f:
        return int(f.readline())


def distro_name() -> str:
    """Returns distro short name"""
    try:
        return _get_os_release()["NAME"]
    except KeyError:
        raise ValueNotFoundError("distro name", _OS_RELEASE, 61)


def distro_full_name() -> str:
    """Returns full distro description"""
    try:
        return _get_os_release()["PRETTY_NAME"]
    except KeyError:
        raise ValueNotFoundError("distro description", _OS_RELEASE, 61)


def distro_version() -> str:
    """Return distro version"""
    try:
        return _get_os_release()["VERSION"]
    except KeyError:
        raise ValueNotFoundError("distro version", _OS_RELEASE, 61)


def distro_url() -> str:
    """Returns distro home url"""
    try:
        return _get_os_release()["HOME_URL"]
    except KeyError:
        raise ValueNotFoundError("distro url", _OS_RELEASE, 61)


def linux_distribution():
    """Returns a tuple with the Linux distribution info (distro id, distro version, version codename)

    Emulation of the output of the linux_distribution() method (deprecated) of sys.platform.
    Unlike sys.platform.linux_distribution, info it's got from /etc/os-release

    """
    info = _get_os_release()
    try:
        return info["ID"], info["VERSION_ID"], info["VERSION_CODENAME"]
    except KeyError as ex:
        key = ex.args[0]
        value = "distro id" if key == "ID" else "distro version" if key == "VERSION_ID" else "version codename"
        raise ValueNotFoundError(value, _OS_RELEASE, 61)
