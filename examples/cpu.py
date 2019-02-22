#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018

from os.path import pardir, realpath
from sys import path
path.append(realpath(pardir))

from statux.cpu import *
from examples._functions import *


print_txt("Physical CPU's", physical_cpus())
print_txt("Logical CPU's", logical_cpus())
print_txt("Max Frequency", max_frequency(False, scale="ghz"), "GHz")

print("\nCPU Load (interval > 0):")
cpu_load = Load()
stat = cpu_load.next_value(interval=1.0, per_core=True, precision=1)
for core in range(len(stat)):
    print("cpu%d: %.1f%%" % (core + 1, stat[core]))


print("\nCPU Load (interval == 0):")
count = 0
while count <= 10:
    print_txt("Current CPU Load", cpu_load.next_value(0.0, False), "%")
    sleep(1)
    count += 1

print("\nCPU Frequency:")
freq = frequency()
freq_percent = frequency_percent()

while count > 0:
    for core in range(logical_cpus()):
        print("Frequency cpu%d: %.3f MHz (%.2f%%)" % (core + 1, freq[core], freq_percent[core]))
    print("")
    sleep(1)
    count -= 1
