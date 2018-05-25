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
    print_txt("Total", get_mem_total(scale), s)
    print_txt("Free", get_mem_free(scale), s)
    print_txt("Available", get_mem_available(scale), s)
    print_txt("Used", get_mem_used(scale), s),
    print_txt("Buff/cache", get_mem_buff_cache(scale), s)
    print_txt("Free", get_mem_free_percent(2), "%")
    print_txt("Available", get_mem_available_percent(), "%")
    print_txt("Used", get_mem_used_percent(), "%")


repeat(10, mem, scale="bytes")
