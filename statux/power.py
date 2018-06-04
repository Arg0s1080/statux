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
_ACAD = "%sACAD/" % _PARENT
_OTHER = "%sOTHER" % _PARENT  # TEST: Prevision
_LID = "/proc/acpi/button/lid/"


def lid_state():
    lid = None
    for folder in listdir(_LID):
        if folder.startswith("LID"):
            lid = folder
    if lid is not None:
        with open(join(_LID, lid, "state"), "r") as f:
            return f.readline().split()[1]


print(lid_state())
