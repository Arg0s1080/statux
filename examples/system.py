#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018

from sys import path
path.append(path[0].replace("examples", ""))

from statux.system import *
from examples._functions import print_txt

print_txt("Boot time", boot_time(str_format=True), "(%d seconds)" % boot_time())
print_txt("Uptime", uptime(str_format=True), "(%d seconds)" % uptime())
print_txt("Init", init())
print_txt("Hostname", hostname())
print_txt("Kernel release", kernel_release())
print_txt("Kernel version", kernel_version())
print_txt("Architecture",architecture())
