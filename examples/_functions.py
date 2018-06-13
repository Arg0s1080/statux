#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018


from time import sleep


def print_txt(description, value, unit="", length=18):
    unit = "" if value is None else unit
    print("%s: %s %s" % ((description + " ").ljust(length, "."), str(value), unit))


def repeat(times, fun, *args, **kwargs):
    for _ in range(times):
        fun(*args, **kwargs)
        sleep(1)

