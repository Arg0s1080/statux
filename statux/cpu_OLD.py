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

from time import sleep
from os import listdir
from os.path import join
from statux._conversions import set_mhz

_PROC = "/proc/"
_STAT = "%sstat" % _PROC
_CPUINFO = "%scpuinfo" % _PROC
_FREQUENCY_POLICY = "/sys/devices/system/cpu/cpufreq/"
_MAX_FREQUENCY = None
_last = None


def _get_stat() -> list:
    with open(_STAT, "rb") as file:
        stat = file.readlines()
        return [list(map(int, stat[line].split()[1:])) for line in range(len(stat)) if stat[line].startswith(b"cpu")]


def logical_cpus() -> int:
    """Return the number of logical processors"""
    return len(_get_stat()) - 1


def physical_cpus() -> int:
    """Return the number of physical processors"""
    # TODO: to get better
    with open(_CPUINFO, "rb") as file:
        res = {}
        stat = file.readlines()
        for i in range(len(stat)):
            if stat[i].startswith(b"physical id"):
                physical_id = stat[i].split()[-1]
                res[physical_id] = int(stat[i+3].split()[-1])
        return sum(res.values())


def load_percent(interval=0.0, per_core=False, precision=2):
    """ Returns CPU load percentage

    :Params:
        :interval (float): Seconds. When value is greater than zero, it returns cpu load percentage
                           in that period of time. When interval value is 0, it returns cpu load
                           percentage since the last call
        :per_core  (bool): When per_core is True it returns a list with values per logical cpu, if
                           it's set to False returns a float with arithmetic mean of cores values.
        :precision  (int): Number of rounding decimals

    """
    global _last
    if _last is None or interval > 0.0:
        old_stat = _get_stat()
        sleep(interval)
    else:
        old_stat = _last
    new_stat = _get_stat()
    _last = new_stat
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
    return res if len(res) > 1 else res[0]


def frequency(per_core=True, scale="mhz", precision=3):
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
        return r if per_core else round(sum(r) / float(len(r)), precision)


def max_frequency(per_core=True, scale="mhz", precision=3):
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
    for policy in listdir(_FREQUENCY_POLICY):
        if policy.startswith("policy"):
            for file in listdir(join(_FREQUENCY_POLICY, policy)):
                if file == "cpuinfo_max_freq":
                    with open(join(_FREQUENCY_POLICY, policy, file), "rb") as stat:
                        r.insert(int(policy[-1]), int(stat.readline()) / 1000)
                    break
    if _MAX_FREQUENCY is None:
        _MAX_FREQUENCY = r
    r = list(map(lambda x: round(set_mhz(x, scale), precision), r))
    return r if per_core else round(sum(r) / float(len(r)), precision)


def frequency_percent(per_core=True, precision=2):
    """Returns current CPU frequency percent

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


def is_64_bit():
    """Returns True if CPU is 64 bit"""
    with open(_CPUINFO, "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            if line.startswith("flags"):
                if "lm" in line.split()[2:]:
                    return True
    return False
