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

_PARENT = "/sys/class/power_supply/"
_STAT = "uevent"
_ACAD = "%sACAD/" % _PARENT
_UPOWER = "/etc/UPower/UPower.conf"
_LID = "/proc/acpi/button/lid/"


def _noner(fun):
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except KeyError:
            return
        except TypeError:
            return
    return wrapper


def _get_stat(stat_: str) -> list:
    bat = None
    if exists(_PARENT):
        for folder in listdir(_PARENT):
            if folder.startswith("BAT"):
                bat = folder
                break
        if bat is not None:
            with open(join(_PARENT, bat, stat_), "r") as f:
                return f.readlines()


def _get_uevent():
        file = _get_stat(_STAT)
        if file is not None:
            res = {}
            for ln in file:
                ln = ln.replace("POWER_SUPPLY_", "").split("=")
                key = ln[0].lower()
                value = ln[1][:-1]
                res[key] = value if not value.isdigit() else int(value)
            return res


def _get_upower():
    def set_dict(line, pattern, percent_):
        ud = "%" if percent_ else "s"
        m = line.replace(pattern, "").split("=")
        res[m[0]] = "%s%s" % (m[1][:-1], ud)

    # TODO Get better
    if exists(_UPOWER):
        with open(_UPOWER, "r") as f:
            file = f.readlines()
            res = {}
            percent = True
            for ln in file:
                if ln.startswith("#") or ln.startswith("\n"):
                    continue
                else:
                    if ln.startswith("UsePercentageForPolicy"):
                        val = ln.split("=")[1][:-1].lower()
                        percent = False if val == "false" else True
                    elif ln.startswith("CriticalPowerAction"):
                        res["PowerAction"] = ln.split("=")[1][:-1]
                    else:
                        if percent:
                            if ln.startswith("Percentage"):
                                set_dict(ln, "Percentage", percent)
                        else:
                            if ln.startswith("Time"):
                                set_dict(ln, "Time", percent)
        return res


stat = _get_uevent()


@_noner
def battery() -> dict:
    """Returns a dict with manufacturer, model and serial number of the battery"""
    return {
        "Manufacturer":  stat["manufacturer"],
        "Model":         str(stat["model_name"]),
        "Serial Number": str(stat["serial_number"])
    }


@_noner
def status() -> str:
    """Returns the status battery (Full, Charging or Discharging)"""
    return stat["status"]


@_noner
def is_present() -> bool:
    """Return True if the battery is present, False otherwise"""
    return bool(stat["present"])


@_noner
def voltage() -> int:
    """Return the battery voltage (mV)"""
    return round(stat["voltage_now"] / 10**3)


@_noner
def current() -> int:
    """Return the battery current (mA)"""
    return round(stat["current_now"] / 10**3)


@_noner
def power() -> int:
    """Return the battery power (mW)"""
    return voltage() * current()


@_noner
def charge() -> int:
    """Returns the current battery charge (mAh)"""
    return round(stat["charge_now"] / 10**3)


@_noner
def capacity() -> int:
    """Return the current percentage of the battery (%)"""
    return stat["capacity"]


@_noner
def capacity_level() -> str:
    """Return the current battery capacity level (Full, Normal, Low or Critical)"""
    return stat["capacity_level"]


@_noner
def low_level() -> str:
    """Returns the value set for low battery level (% or seconds)"""
    return _get_upower()["Low"]


@_noner
def critical_level() -> str:
    """Returns the value set for critical battery (% or seconds)"""
    return _get_upower()["Critical"]


@_noner
def action_level() -> str:
    """Returns the value of the critical power action level (% or seconds)"""
    return _get_upower()["Action"]


@_noner
def critical_power_action() -> str:
    """Returns critical power action (PowerOff, Hibernate or HybridSleep)"""
    return _get_upower()["PowerAction"]


@_noner
def remaining_time(format=True) -> object:
    """Returns remaining battery life

    Param:
        format (bool): If format is False returns remaining seconds, a time format string (H:M) otherwise
        """
    current_now = current()
    try:
        value = charge() / current_now
        return "%d:%02d" % (int(value), round((value - int(value)) * 60)) if format else round(value * 3600)
    except ZeroDivisionError:
        return None


@_noner
def wear_level() -> float:
    """Returns the wear level of the battery (%)

    It's a health indicator of the battery (less is better)
    """
    return round(100 - (stat["charge_full"] / stat["charge_full_design"] * 100), 2)


@_noner
def technology() -> str:
    """Returns chemistry of the battery"""
    return stat["technology"]


@_noner
def supply_type():
    return _get_stat("type")[0]


@_noner
def lid_state():
    lid = None
    for folder in listdir(_LID):
        if folder.startswith("LID"):
            lid = folder
    if lid is not None:
        with open(join(_LID, lid, "state"), "r") as f:
            return f.readline().split()[1]

# YOU ARE HERE if not exists uvent, type, lid, etc (file and paths)
print(supply_type())