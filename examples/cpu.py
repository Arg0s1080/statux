#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018

from sys import path
path.append(path[0].replace("examples", ""))

from statux.cpu import *
from examples._functions import *


print_txt("Physical CPU's", physical_cpus())
print_txt("Logical CPU's", logical_cpus())
print_txt("Max Frequency", max_frequency(False, scale="ghz"), "GHz")

print("\nCPU Load (interval > 0):")
stat = load_percent(interval=1.0, per_core=True, precision=1)
for cpu in range(len(stat)):
    print("cpu%d: %.1f%%" % (cpu + 1, stat[cpu]))


print("\nCPU Load (interval == 0):")
count = 0
while count <= 10:
    print_txt("Current CPU Load", load_percent(0.0, False), "%")
    sleep(1)
    count += 1

print("\nCPU Frequency:")
freq = frequency()
freq_percent = frequency_percent()

while count > 0:
    for cpu in range(logical_cpus()):
        print("Frequency cpu%d: %.3f MHz (%.2f%%)" % (cpu+1, freq[cpu], freq_percent[cpu]))
    print("")
    sleep(1)
    count -= 1
