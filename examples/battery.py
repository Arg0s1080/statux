#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018


from statux.battery import *
from examples.functions import print_txt


if is_present():

    for k, v in battery().items():
        print_txt(k, v)

    print_txt("Supply type", supply_type())
    print_txt("Status", status())
    print_txt("Remaining Time", remaining_time())
    print_txt("Remaining Time", remaining_time(format=False), "seconds")
    print_txt("Voltage", voltage(), "mV")
    print_txt("Current", current(), "mA")
    print_txt("Power", power(), "mW")
    print_txt("Charge", charge(), "mAh")
    print_txt("Capacity", capacity(), "%")
    print_txt("Capacity level", capacity_level())
    print_txt("Wear level", wear_level(), "%")
    print_txt("Chemistry", technology())
    print_txt("Low level", low_level())
    print_txt("Action level", action_level())
    print_txt("Power action", critical_power_action())

lid = lid_state()
if lid is not None:
    print(" \nLid is %s" % lid)
