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

from os import listdir
from os.path import join
from statux._conversions import set_mhz
from statux._errors import *
from time import sleep
from typing import Union, List


_PROC_PTH = "/proc/"
_STAT = "%sstat" % _PROC_PTH
_CPUINFO = "%scpuinfo" % _PROC_PTH
_UPTIME = "%suptime" % _PROC_PTH
_FREQUENCY_POLICY = "/sys/devices/system/cpu/cpufreq/"
_MAX_FREQUENCY = None  # MHz


def _has_flag(flag: str) -> bool:
    def flags():
        with open(_CPUINFO, "r") as f:
            for line in f:
                if line.startswith("flags"):
                    return line.split()[2:]
    return flag in flags()


@ex_handler(_STAT, "CPU load")
class Load:
    """ Class to get CPU Load Percentage.

            :Params:
                :initialize (bool): When initialize is True, next_value() is called to set self._last.
                                    Useful, for example, if Load() is instantiated and after next_value()
                                    is called from a timer. next_value() will return a value != 0.0 in
                                    the first "tick"


    It allows obtaining several percentage CPU load values in the same time interval instantiating
    the class.
    """
    def __init__(self, initialize=False):
        self._last = None
        initialize and self.next_value()

    @staticmethod
    def _get_stat() -> list:
        with open(_STAT, "rb") as file:
            stat = file.readlines()
            return [list(map(int, stat[line].split()[1:])) for line in range(len(stat))
                    if stat[line].startswith(b"cpu")]

    def next_value(self, interval=0.0, per_core=False, precision=2) -> Union[float, List[float]]:
        """ Returns CPU load percentage

        :Params:
            :interval (float): Seconds. When value is greater than zero, it returns cpu load percentage
                              in that period of time. When interval value is 0, it returns cpu load
                              percentage since the last call
            :per_core  (bool): When per_core is True it returns a list with values per logical cpu, if
                              it's set to False returns a float with arithmetic mean of cores values.
            :precision  (int): Number of rounding decimals

        """
        if self._last is None or interval > 0.0:
            old_stat = self._get_stat()
            sleep(interval)
        else:
            old_stat = self._last
        new_stat = self._get_stat()
        self._last = new_stat
        if per_core:
            old_stat = old_stat[1:]
            new_stat = new_stat[1:]
        else:
            old_stat = old_stat[0:1]
            new_stat = new_stat[0:1]

        res = []
        for cpu in range(len(old_stat)):
            old_active = old_stat[cpu][:]
            old_active[3:5] = []
            new_active = new_stat[cpu][:]
            new_active[3:5] = []

            old_total = sum(old_stat[cpu])
            new_total = sum(new_stat[cpu])

            total_dif = new_total - old_total
            active_dif = sum(new_active) - sum(old_active)

            res.append(round(active_dif / total_dif * 100, precision) if total_dif != 0 else 0.0)
        len_ = len(res)
        if len_ < 1:
            raise ValueNotFoundError("CPU Load", _STAT, errno.ENODATA)
        return res if len_ > 1 else res[0]

    def __len__(self):
        return len(self._get_stat()) - 1


def logical_cpus() -> int:
    return len(Load())


@ex_handler(_CPUINFO)
def physical_cpus() -> int:
    """Return the number of physical processors"""
    # TODO: to get better
    with open(_CPUINFO, "rb") as file:
        res = {}
        stat = file.readlines()
        for i in range(len(stat)):
            if stat[i].startswith(b"physical id"):
                physical_id = int(stat[i].split()[-1])
                res[physical_id] = int(stat[i+3].split()[-1])
        if not len(res):
            raise ValueNotFoundError("physical cpu's", _CPUINFO, errno.ENODATA)
        return sum(res.values())


def frequency(per_core=True, scale="mhz", precision=3) -> Union[float, List[float]]:
    """Returns current cpu frequency

    :Params:
        :per_core (bool): When per_core is True it returns a list with values per logical cpu,
                          if it's set to False returns a float with arithmetic mean of cores
                          values.
        :scale     (str): Return scale (Hz, KHz, MHz or GHz). MHz by default. Case insensitive
        :precision (int): Number of rounding decimals

    """

    with open(_CPUINFO, "rb") as file:
        stat = file.readlines()
        r = [round(set_mhz(float(line.split()[-1]), scale), precision) for line in stat if line.startswith(b"cpu MHz")]
        if not len(r):
            raise(ValueNotFoundError("cpu frequency", _CPUINFO, errno.ENODATA))
        return r if per_core else round(sum(r) / float(len(r)), precision)


def max_frequency(per_core=True, scale="mhz", precision=3) -> Union[float, List[float]]:
    """Returns cpu max frequency

        :Params:
            :per_core (bool): When per_core is True it returns a list with values per logical cpu,
                              if it's set to False returns a float with arithmetic mean of cores
                              values.
            :scale     (str): Return scale (Hz, KHz, MHz or GHz). MHz by default. Case insensitive
            :precision (int): Number of rounding decimals

        """
    global _MAX_FREQUENCY
    r = []
    err_no = 0
    if _MAX_FREQUENCY is None:
        try:
            for policy in listdir(_FREQUENCY_POLICY):
                if policy.startswith("policy"):
                    for file in listdir(join(_FREQUENCY_POLICY, policy)):
                        if file == "cpuinfo_max_freq":
                            with open(join(_FREQUENCY_POLICY, policy, file), "rb") as stat:
                                r.insert(int(policy[-1]), int(stat.readline()) / 1000)
                            break
        except ValueError:
            err_no = errno.ENODATA
        err_no = errno.ENOENT if not len(r) else err_no
        if err_no:
            raise ValueNotFoundError("cpu max frequency", _FREQUENCY_POLICY, err_no)
        _MAX_FREQUENCY = r  # MHz
    else:
        r = _MAX_FREQUENCY
    rs = list(map(lambda x: round(set_mhz(x, scale), precision), r))
    return rs if per_core else round(sum(rs) / float(len(rs)), precision)


def frequency_percent(per_core=True, precision=2) -> Union[float, List[float]]:
    """Returns current cpu frequency percent

        :Params:
            :per_core (bool): When per_core is True it returns a list with values per logical cpu,
                              if it's set to False returns a float with arithmetic mean of cores
                              values.
            :precision (int): Number of rounding decimals. 2 by default.

    """
    global _MAX_FREQUENCY
    mxm = max_frequency() if _MAX_FREQUENCY is None else _MAX_FREQUENCY
    r = [round(c / m * 100, precision) for c, m in zip(frequency(), mxm)]
    return r if per_core else round(sum(r) / float(len(r)), precision)


def is_x86_64() -> bool:
    """Returns True if CPU is AMD64 or Intel64 i.e. 64 bit capable"""
    return _has_flag("lm")


def model_name() -> Union[str, List[str]]:
    """Returns CPU model name

    If there are more than one physical id with several models names, a list with its names
    will be returned.
    """
    r = []
    with open(_CPUINFO) as f:
        for line in f:
            if line.startswith("model name"):
                r.append(line[line.find(": ")+2:-1])
    result = list(set(r))  # Removing duplicated items
    return r[0] if len(result) == 1 else result
