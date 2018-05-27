#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018


from statux.ram import *
from examples.functions import *


def mem(scale):
    s = scale if scale != "auto" else ""
    print("RAM")
    print_txt("Total", total(scale), s)
    print_txt("Free", free(scale), s)
    print_txt("Available", available(scale), s)
    print_txt("Used", used(scale), s),
    print_txt("Buff/cache", buff_cache(scale), s)
    print_txt("Free", free_percent(2), "%")
    print_txt("Available", available_percent(), "%")
    print_txt("Used", used_percent(), "%")


repeat(10, mem, scale="bytes")
