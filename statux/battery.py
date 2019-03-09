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

# NOTE: THIS CODE IS VALID FOR MOST LAPTOPS. IN CASE OF HAVING MORE THAN ONE SUPPLY,
#       ONLY THE FIRST ONE WILL BE DETECTED
# TODO: *1st* Find out how its work in desktop
# TODO: Handle exceptions

from os import listdir
from os.path import join
from statux._errors import ValueNotFoundError, errno, strerror


_PARENT = "/sys/class/power_supply/"
_UEVENT = "uevent"
_UPOWER = "/etc/UPower/UPower.conf"
_LID = "/proc/acpi/button/lid/"
_PTH = None


def ex_handler(fun):
    def wrapper(*args, **kwargs):
        def get_name():
            # Returns method name
            return fun.__name__.replace("_", " ")
        error = None
        msg = None
        try:
            return fun(*args, **kwargs)
        except FileNotFoundError:
            error = errno.ENOENT
            msg = strerror(error)
        except KeyError:
            error = errno.ENODATA
            msg = strerror(error)
        except TypeError as exc:
            error = errno.ENOMSG
            msg = "%s: %s" % (strerror(errno.ENOMSG), exc.args[0])
        except ValueError as exc:
            error = errno.ENOMSG
            msg = "%s: %s" % (strerror(errno.ENOMSG), exc.args[0])
        finally:
            if error is not None:
                raise ValueNotFoundError(get_name(), _PTH, err_no=error, msg=msg)
    return wrapper


def _get_stat(file: str, supply: str) -> list:
    # supply: can be "BAT0", "BAT1", "ACAD", "UPS"...
    global _PTH
    supply_ = None
    _PTH = _PARENT
    # TODO: More than one supply support
    for supply_ in [folder for folder in listdir(_PARENT)]:  # for supply in supplies
        if supply_.startswith(supply):
            break  # First supply is chosen
    _PTH = join(_PARENT, supply_, file)
    if supply_ is not None:
        with open(_PTH, "r") as f:
            return f.readlines()


def _get_uevent(supply: str):
    # supply: can be "BAT0", "BAT1", "ACAD", "UPS"...
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
    raise KeyError


def _get_upower():
    def set_dict(line, pattern, percent_):
        ud = "%" if percent_ else "s"
        m = line.replace(pattern, "").split("=")
        res[m[0]] = "%s%s" % (m[1][:-1], ud)
    global _PTH
    _PTH = _UPOWER
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

@ex_handler
def battery() -> dict:
    """Returns a dict with manufacturer, model and serial number of the battery"""
    stat = _get_values()
    return {
        "Manufacturer":  stat["manufacturer"],
        "Model":         str(stat["model_name"]),
        "Serial Number": str(stat["serial_number"])
    }


@ex_handler
def status() -> str:
    """Returns the status battery ('Full', 'Charging' or 'Discharging')"""
    return _get_value("status")


@ex_handler
def is_present() -> bool:
    """Return True if the battery is present, False otherwise"""
    return bool(int(_get_value("present")))


@ex_handler
def voltage() -> int:
    """Return the battery voltage (mV)"""
    return round(_get_value("voltage_now") / 10**3)


@ex_handler
def current() -> int:
    """Return the battery current (mA)"""
    current_ = _get_value("current_now")
    if current_ is None:  # current value is not given...
        stat = _get_values()
        power_, voltage_ = stat["power_now"], stat["voltage_now"]  # so, let's try to get power and voltage
        return round(power_ / voltage_ * 10**3)
    return round(current_ / 10**3)


@ex_handler
def energy() -> int:
    """Returns the battery energy value (mWh)"""
    try:
        energy_ = _get_value("energy_now")
        return round(energy_ / 10**3)
    except KeyError:  # energy value is not given...
        stat = _get_values()
        voltage_, charge_ = stat["voltage_now"], stat["charge_now"]  # so let's try to get voltage and charge
        return round(voltage_ * charge_ / 10 ** 9)


@ex_handler
def power() -> int:
    """Return the battery power (mW)"""
    stat = _get_values()
    try:
        voltage_, current_ = stat["voltage_now"], stat["current_now"]
    except KeyError:
        return round(stat["power_now"] / 10 ** 3)
    return round(voltage_ * current_ / 10 ** 9)


@ex_handler
def charge() -> int:
    """Returns the current battery charge (mAh)"""
    try:
        charge_ = _get_value("charge_now")
        return round(charge_ / 10**3)
    except KeyError:  # charge value is not given...
        stat = _get_values()
        energy_, voltage_ = stat["energy_now"], stat["voltage_now"]
        return round(energy_ / voltage_ * 10**3)


@ex_handler
def capacity() -> int:
    """Return the current percentage of the battery (%)"""
    return _get_value("capacity")


@ex_handler
def capacity_level() -> str:
    """Return the current battery capacity level ('Full', 'Normal', 'Low' or 'Critical')"""
    return _get_value("capacity_level")


@ex_handler
def low_level() -> str:
    """Returns the value set for low battery level (% or seconds)"""
    return _get_upower()["Low"]


@ex_handler
def critical_level() -> str:
    """Returns the value set for critical battery (% or seconds)"""
    return _get_upower()["Critical"]


@ex_handler
def action_level() -> str:
    """Returns the value of the critical power action level (% or seconds)"""
    return _get_upower()["Action"]


@ex_handler
def critical_power_action() -> str:
    """Returns critical power action ('PowerOff', 'Hibernate' or 'HybridSleep')"""
    return _get_upower()["PowerAction"]


@ex_handler
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


@ex_handler
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


@ex_handler
def technology() -> str:
    """Returns chemistry of the battery"""
    return _get_value("technology")


@ex_handler
def supply_type():
    """Returns type of supply ('Battery', 'Mains', 'UPS', etc)"""
    try:
        return _get_stat("type", supply="BAT")[0][:-1]
    except IndexError:
        raise ValueNotFoundError("supply type", _PTH, 61)


##############
# MISCELLANY:
##############


def lid_state():
    """Returns lid state ('Open' or 'Close')"""
    lid = None
    error = None
    try:
        for folder in listdir(_LID):
            if folder.startswith("LID"):
                lid = folder
                break
        if lid is not None:
            with open(join(_LID, lid, "state"), "r") as f:
                return f.readline().split()[1]
        else:
            error: errno.ENODATA
    except FileNotFoundError:
        error = errno.ENOENT
    finally:
        if error is not None:
            raise ValueNotFoundError("lid state", _LID, error)


@ex_handler
def ac_adapter_online() -> bool:
    """Returns True if AC adapter is online, False otherwise"""
    return bool(int(_get_value("online", supply="ACAD")))
