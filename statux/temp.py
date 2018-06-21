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
from os.path import join, exists
from statux._conversions import set_celsius

_PARENT = "/sys/devices/platform/coretemp.0/hwmon/"
_HWMON = "hwmon"


def _get_stat():
    res = {}
    if exists(_PARENT):
        parent_path = _PARENT
    else:
        parent_path = "/sys/class/hwmon/"  # in some AMD _PARENT doesn't exist
    for hwmon in listdir(parent_path):
        for file in listdir(join(parent_path, hwmon)):
            if file.endswith("label"):
                path_l = join(parent_path, hwmon, file)
                with open(path_l, "rb") as file_l:
                    label = file_l.readline()[:-1]
                    with open(path_l.replace("label", "input"), "rb") as file_t:
                        res[label.decode()] = int(file_t.readline()[:-1])
    return res


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
        if " id" in key:
            return set_celsius(stat[key], scale, precision)


def max_val(scale="celsius", precision=2) -> float:
    """Returns the maximum value of the temp sensors obtained

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals
    """
    stat = _get_stat()
    return set_celsius(max(stat.values()), scale, precision)
