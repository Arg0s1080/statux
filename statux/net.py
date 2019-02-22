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
from statux._conversions import set_bytes
from statux._errors import ValueNotFoundError


_STAT_PATH = "/proc/net/dev"
_last = None


def _get_stat():
    with open(_STAT_PATH, "r") as file:
        stat = file.readlines()
        res = {}
        for i in range(2, len(stat)):
            ln = stat[i].split()
            res[ln[0][:-1]] = (int(ln[1]), int(ln[9]))
        return res


def _check_interface(interface: str, stat: dict):
    if interface not in stat.keys():
        raise ValueNotFoundError(interface, _STAT_PATH, errno.ENODEV)
    return interface


def _get_bytes(interface: str, direction: int):
    # param direction:  Download: 0, Upload: 1, Both: 2
    stat = _get_stat()
    _check_interface(interface, stat)
    for key, value in stat.items():
        if key == interface:
            return value[direction] if direction != 2 else value


def _set_delta(interface: str, interval=0.0):
    # Speed average per second
    # param direction:  Download: 0, Upload: 1
    from time import sleep, time
    global _last
    if _last is None or interval > 0.0:
        # print("Debug. Sleeping %d seconds" % interval)
        old_stat = _get_stat()
        sleep(interval)
        elapsed = interval
    else:
        # print("Debug. Not sleeping")
        old_stat = _last[0]
        elapsed = round(time() - _last[1], 3)  # milliseconds
    new_stat = _get_stat()
    _check_interface(interface, new_stat)
    _last = new_stat, time()
    delta = new_stat[interface][0] - old_stat[interface][0], new_stat[interface][1] - old_stat[interface][1]
    return (0.0, 0.0) if not elapsed else (delta[0] / elapsed, delta[1] / elapsed)


def get_interfaces() -> list:
    """Returns a list with all network interfaces"""
    res = []
    for item in _get_stat().keys():
        res.append(item)
    return res


def download_bytes(interface: str, scale="bytes", precision=2):
    """Returns total bytes downloaded in the given interface

        :Params:
            :interface (str): Interface name
            :scale     (str): Return scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
            :precision (int): Number of rounding decimals

    """
    return set_bytes(_get_bytes(interface, 0), scale_in="bytes", scale_out=scale, precision=precision)


def upload_bytes(interface: str, scale="bytes", precision=2):
    """Returns total bytes uploaded in the given interface

        :Params:
            :interface (str): Interface name
            :scale     (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, MB, GB, TB or auto)
            :precision (int): Number of rounding decimals

    """
    return set_bytes(_get_bytes(interface, 1), scale_in="bytes", scale_out=scale, precision=precision)


def down_up_bytes(interface: str, scale="bytes", precision=2):
    """Returns a tuple with bytes down-uploaded in the given interface

        :Params:
            :interface (str): Interface name
            :scale     (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, MB, GB, TB or auto)
            :precision (int): Number of rounding decimals

    """
    bytes_ = _get_bytes(interface, 2)
    return set_bytes(*bytes_, scale_in="bytes", scale_out=scale, precision=precision)


def download_speed(interface: str, interval=0.0, scale="bytes", precision=2):
    """Returns average download speed per second in the given interface

        :Params:
            :interface  (str): Interface name
            :interval (float): Interval in seconds.
            :scale      (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, Mb, GB, TB or auto)
            :precision  (int): Number of rounding decimals

    """

    return set_bytes(_set_delta(interface, interval)[0], scale_in="bytes", scale_out=scale, precision=precision)


def upload_speed(interface: str, interval=0.0, scale="bytes", precision=2):
    """Returns average upload speed per second in the given interface

        :Params:
            :interface  (str): Interface name
            :interval (float): Interval in seconds.
            :scale      (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, Mb, GB, TB or auto)
            :precision  (int): Number of rounding decimals

    """

    return set_bytes(_set_delta(interface, interval)[1], scale_in="bytes", scale_out=scale, precision=precision)


def down_up_speed(interface: str, interval=0.0, scale="bytes", precision=2):
    """Returns a tuple with average download-upload speed per second in the given interface

        :Params:
            :interface  (str): Interface name
            :interval (float): Interval in seconds.
            :scale      (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, Mb, GB, TB or auto)
            :precision  (int): Number of rounding decimals
    """

    stat = _set_delta(interface, interval)
    return set_bytes(stat[0], stat[1], scale_in="bytes", scale_out=scale, precision=precision)

