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

_PARENT = "/proc/"
_STAT = "%sstat" % _PARENT
_CPUINFO = "%scpuinfo" % _PARENT
_UPTIME = "%suptime" % _PARENT
_PARENT = "/proc/"
_FREQUENCY_POLICY = "/sys/devices/system/cpu/cpufreq/"
_MAX_FREQUENCY = None


class Load:
    """Modification of statux.cpu made for Pycket project.

    It allows obtaining several percentage load values in the same time interval instantiating the class"""
    def __init__(self):
        self._last = None
        self.next_value()  # The method is called to set self._last

    @staticmethod
    def _get_stat() -> list:
        with open(_STAT, "rb") as file:
            stat = file.readlines()
            return [list(map(int, stat[line].split()[1:])) for line in range(len(stat))
                    if stat[line].startswith(b"cpu")]

    def next_value(self, interval=0.0, per_core=False, precision=2):
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
        return res if len(res) > 1 else res[0]

    def __len__(self):
        return len(self._get_stat())


def logical_cpus() -> int:
    """Return the number of logical processors"""
    return len(Load()) - 1


def physical_cpus():
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


def boot_time(str_format=False):
    """Returns the time at which the system booted

        :Params:
            str_format (bool): If is False returns seconds since the Unix epoch (January 1, 1970),
                               if is set to True returns a formatted string with the system boot
                               time. False by default.
    """
    def sformat(v):
        from time import strftime, localtime
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
    from datetime import timedelta
    with open(_UPTIME, "rb") as f:
        sec = float(f.readline().split()[0])
        return str(timedelta(seconds=sec)).rstrip("0").rstrip(".") if str_format else sec
