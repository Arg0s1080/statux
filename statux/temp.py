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
from os.path import join, exists
from statux._conversions import set_celsius
from statux._errors import TempNotFoundError, ValueNotFoundError

_PTH1 = "/sys/devices/platform/coretemp.0/hwmon/"
_PTH2 = "/sys/class/hwmon/"
_PARENT = _PTH1 if exists(_PTH1) else _PTH2  # in some AMD _PTH1 doesn't exist
_HWMON = "hwmon"


def _get_stat():
    # Look for temp#* files in hwmon folders and associate labels with their inputs.
    # E.g. temp1_label.read() = "Package id 0" and temp1_input.read() = "4500"
    #      temp2_label.read() = "Core 0"       and temp2_input.read() = "4100"
    #      will return {"Core 0": 41000, 'Package id 0': 45000}
    res = {}
    err = None
    for hwmon in listdir(_PARENT):
        for file in listdir(join(_PARENT, hwmon)):
            if file.endswith("label"):
                path_l = join(_PARENT, hwmon, file)
                with open(path_l, "rb") as file_l:
                    label = file_l.readline()[:-1].decode()
                    path_i = path_l.replace("label", "input")
                    try:
                        with open(path_i, "rb") as file_i:
                            res[label] = int(file_i.readline()[:-1])
                    except ValueError:
                        err = 42
                    except FileNotFoundError:
                        err = 2
                    finally:
                        if err is not None:
                            raise ValueNotFoundError("%s value" % label, path_i, err)

    return res


def cores(scale="celsius", precision=2) -> list:
    """Returns a sorted list with digital thermal sensors values for each core

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals
    """
    stat = _get_stat()
    if len(stat) > 0:
        return [set_celsius(stat[key], scale, precision) for key in sorted(stat) if key.startswith("Core")]
    raise TempNotFoundError("cores", "cores temp values not found")


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
    raise TempNotFoundError("package id")


def max_val(scale="celsius", precision=2) -> float:
    """Returns the maximum value of the temp sensors obtained

    :Params:
        :scale     (str): Return scale Celsius, Fahrenheit, Kelvin or Rankine)
        :precision (int): Number of rounding decimals
    """
    stat = _get_stat()
    if len(stat) > 0:
        return set_celsius(max(stat.values()), scale, precision)
    raise TempNotFoundError("max value", "no temp value found")
