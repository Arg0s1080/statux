#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2019

from os.path import pardir, realpath
from sys import path
path.append(realpath(pardir))

from statux.system import *
from examples._functions import print_txt
print_txt("User", user())
print_txt("Hostname", hostname())
print_txt("Boot time", boot_time(str_format=True), "(%d seconds)" % boot_time())
print_txt("Uptime", uptime(str_format=True), "(%d seconds)" % uptime())
print_txt("Init", init())
print_txt("Display protocol", display_protocol())
print_txt("System language", system_language())
print_txt("Current desktop", current_desktop())
print_txt("Kernel release", kernel_release())
print_txt("Kernel version", kernel_version())
print_txt("Architecture", architecture())
print_txt("Session ID", session_id())
print_txt("Distro name", distro_name())
print_txt("Distro full name", distro_full_name())
print_txt("Distro version", distro_version())
print_txt("Distro url", distro_url())
did, version, codename = linux_distribution()
print_txt("Distro id", did)
print_txt("Distro version id", version)
print_txt("Distro codename", codename)
