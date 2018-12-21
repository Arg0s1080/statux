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

# NOTE: THIS CODE IS VALID FOR MOST LAPTOPS. IN CASE OF HAVING MORE THAN ONE SUPPLY,
#       ONLY THE FIRST ONE WILL BE DETECTED
# TODO: *1st* Find out how its work in desktop
# TODO: Handle exceptions

from os import listdir
from os.path import join, exists
from statux._errors import *


_PARENT = "/sys/class/power_supply/"
_UEVENT = "uevent"
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


def _get_stat(file: str, supply: str) -> list:
    supply_ = None
    try:
        # TODO: More than one supply support
        for supply_ in [folder for folder in listdir(_PARENT)]:  # for supply in supplies
            if supply_.startswith(supply):
                break  # First supply is chosen
        if supply_ is not None:
            with open(join(_PARENT, supply_, file), "r") as f:
            # TODO: Delete lines below
            #with open("/home/ivan/Escritorio/uevent_BAT0_Fedora_VBox_discharging.fake") as f:
            #with open("/home/ivan/Escritorio/uevent_BAT1_Neon.fake") as f:
                return f.readlines()
    except FileNotFoundError:
        # TODO: Handle exception
        raise


def _get_uevent(supply: str):
    file = _get_stat(_UEVENT, supply)
    if file is not None:
        for ln in file:
            ln = ln.replace("POWER_SUPPLY_", "").split("=")
            v = ln[1][:-1]
            yield ln[0].lower(), v if not v.isdigit() else int(v)


def _get_values(supply="BAT"):
    return {key: value for key, value in _get_uevent(supply)}


def _get_value(item: str, supply="BAT"):
    for key, value in _get_uevent(supply):
        if key == item:
            return value


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


####################
# BATTERY METHODS:
####################


# @_noner
def battery() -> dict:
    """Returns a dict with manufacturer, model and serial number of the battery"""
    stat = _get_values()
    return {
        "Manufacturer":  stat["manufacturer"],
        "Model":         str(stat["model_name"]),
        "Serial Number": str(stat["serial_number"])
    }


# @_noner
def status() -> str:
    """Returns the status battery ('Full', 'Charging' or 'Discharging')"""
    return _get_value("status")


def is_present() -> bool:
    """Return True if the battery is present, False otherwise"""
    return bool(_get_value("present"))


# @_noner
def voltage() -> int:
    """Return the battery voltage (mV)"""
    return round(_get_value("voltage_now") / 10**3)


# @_noner
def current() -> int:
    """Return the battery current (mA)"""
    current_ = _get_value("current_now")
    if current_ is None:  # current value is not given...
        stat = _get_values()
        power_, voltage_ = stat["power_now"], stat["voltage_now"]  # so, let's try to get power and voltage
        return round(power_ / voltage_ * 10**3)
    return round(current_ / 10**3)


# @_noner
def energy() -> int:
    """Returns the battery energy value (mWh)"""
    energy_ = _get_value("energy_now")
    if energy_ is None:  # energy value is not given...
        stat = _get_values()
        voltage_, charge_ = stat["voltage_now"], stat["charge_now"]  # so let's try to get voltage and charge
        return round(voltage_ * charge_ / 10**9)
    return round(energy_ / 10**3)


# @_noner
def power() -> int:
    """Return the battery power (mW)"""
    stat = _get_values()
    try:
        voltage_, current_ = stat["voltage_now"], stat["current_now"]
    except KeyError:
        return round(stat["power_now"] / 10 ** 3)
    return round(voltage_ * current_ / 10 ** 9)


# @_noner
def charge() -> int:
    """Returns the current battery charge (mAh)"""
    charge_ = _get_value("charge_now")
    if charge_ is None:  # charge value is not given...
        stat = _get_values()
        energy_, voltage_ = stat["energy_now"], stat["voltage_now"]
        return round(energy_ / voltage_ * 10**3)
    return round(charge_ / 10**3)


# @_noner
def capacity() -> int:
    """Return the current percentage of the battery (%)"""
    return _get_value("capacity")


# @_noner
def capacity_level() -> str:
    """Return the current battery capacity level ('Full', 'Normal', 'Low' or 'Critical')"""
    return _get_value("capacity_level")


# @_noner
def low_level() -> str:
    """Returns the value set for low battery level (% or seconds)"""
    return _get_upower()["Low"]


# @_noner
def critical_level() -> str:
    """Returns the value set for critical battery (% or seconds)"""
    return _get_upower()["Critical"]


# @_noner
def action_level() -> str:
    """Returns the value of the critical power action level (% or seconds)"""
    return _get_upower()["Action"]


# @_noner
def critical_power_action() -> str:
    """Returns critical power action ('PowerOff', 'Hibernate' or 'HybridSleep')"""
    return _get_upower()["PowerAction"]


# @_noner
def remaining_time(format_time=False):
    """Returns remaining battery life

    :Param:
        :format (bool): If format is False returns remaining seconds, a time format string (H:M) otherwise

    """
    stat = _get_values()
    try:
        dividend, divider, voltage_ = stat["charge_now"], stat["current_now"], stat["voltage_now"]
    except KeyError:
        dividend, divider, voltage_ = stat["energy_now"], stat["power_now"], stat["voltage_now"]
    na = stat["status"] != "Discharging" or (voltage_ > 0 and divider == 0)
    value = not na and dividend / divider
    return (float("inf") if na else "%d:%02d" % (int(value), round((value - int(value)) * 60)) if format_time
            else round(value * 3600))


# @_noner
def wear_level() -> float:
    """Returns the wear level of the battery (%)

    It's a health indicator of the battery (less is better)

    """
    stat = _get_values()
    try:  # Let's try to get charge values
        full, design = stat["charge_full"], stat["charge_full_design"]
    except KeyError:
        full, design = stat["energy_full"], stat["energy_full_design"]
    return round(100 - (full / design * 100), 2)


# @_noner
def technology() -> str:
    """Returns chemistry of the battery"""
    return _get_value("technology")


def supply_type():
    """Returns type of supply ('Battery', 'Mains', 'UPS', etc)"""
    try:
        return _get_stat("type", supply="BAT")[0][:-1]
    except IndexError:
        # TODO: Handle exception
        return

##############
# MISCELLANY:
##############


def lid_state():
    """Returns lid state ('Open' or 'Close')"""
    lid = None
    try:
        for folder in listdir(_LID):
            if folder.startswith("LID"):
                lid = folder
        if lid is not None:
            with open(join(_LID, lid, "state"), "r") as f:
                return f.readline().split()[1]
    except FileNotFoundError:
        # TODO: Handle exception
        return


# @_noner
def ac_adapter_online() -> bool:
    """Returns True if AC adapter is online, False otherwise"""
    return bool(_get_value("online", supply="ACAD"))

