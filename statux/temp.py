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


from os import listdir
from os.path import join
from statux._conversions import set_celsius

_PKG_INPUT = "/sys/class/thermal/"
_PARENT = "/sys/devices/platform/"
_STAT = "hwmon"


def _get_stat():
    # Only one physical id
    res = {}
    stat_path = join(_PARENT, "coretemp.0", _STAT)
    for path in listdir(stat_path):
        for file in listdir(join(stat_path, path)):
            if file.endswith("label"):
                path_l = join(stat_path, path, file)
                with open(path_l, "rb") as file_l:
                    label = file_l.readline()[:-1]
                    with open(path_l.replace("label", "input"), "rb") as file_t:
                        res[label.decode()] = int(file_t.readline()[:-1])
    return res


def _get_stat_multi_physical_id():
    # Experimental: Created to work with more than one physical id
    res = {}
    ids = []
    for coretemp in listdir(_PARENT):
        if coretemp.startswith("coretemp"):
            stat_path = join(_PARENT, coretemp, _STAT)
            for path in listdir(stat_path):
                cores = {}
                for file in listdir(join(stat_path, path)):
                    if file.endswith("label"):
                        path_l = join(stat_path, path, file)
                        with open(path_l, "rb") as file_l:
                            label = file_l.readline()[:-1]
                            ls = label.split()
                            if len(ls) > 2 and ls[1] == b"id":
                                ids.append(int(ls[2]))
                            # else:  # Uncomment and indent to get core temps only
                            with open(path_l.replace("label", "input"), "rb") as file_t:
                                cores[label] = int(file_t.readline()[:-1])
                for id_ in ids:
                    res["Physical id %d" % id_] = cores
    return res


def x86_pkg(scale="celsius", precision=2) -> float:
    """Returns CPU digital temperature package level sensor value

    More info: https://www.kernel.org/doc/Documentation/thermal/x86_pkg_temperature_thermal

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals
    """
    for path in listdir(_PKG_INPUT):
        if path.startswith("thermal_zone"):
            with open(join(_PKG_INPUT, path, "type"), "rb") as f:
                if b"x86_pkg_temp" in f.read():
                    return set_celsius(float(open(join(_PKG_INPUT, path, "temp")).readline()), scale, precision)


def cores(scale="celsius", precision=2) -> list:
    """Returns a sorted list with digital thermal sensors values for each core

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals
    """
    stat = _get_stat()
    return [set_celsius(stat[key], scale, precision) for key in sorted(stat) if key.startswith("Core")]


def cpu(scale="celsius", precision=2) -> float:
    """Returns measured value on the surface of the integrated heat spreader, also called CPU temperature

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals
    """
    stat = _get_stat()
    for key in stat:
        if not key.startswith("Core"):
            return set_celsius(stat[key], scale, precision)


def cores_multi(scale="celsius", precision=2) -> dict:
    """Returns a dict with digital thermal sensors values for each core. Each dict key is a physical id

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals

    Note: Experimental
    """
    stat = _get_stat_multi_physical_id()
    sc = lambda v: set_celsius(v, scale, precision)
    return {key: [sc(stat[key][k]) for k in sorted(stat[key]) if k.startswith(b"Core")] for key in sorted(stat)}


def cpu_multi(scale="celsius", precision=2) -> dict:
    """Returns a dict with measured values on each surface of the integrated heat spreaders

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals

    Note: Experimental
    """
    s = _get_stat_multi_physical_id()
    return {key: [set_celsius(s[key][k], scale, precision) for k in sorted(s[key]) if b"id" in k] for key in sorted(s)}

