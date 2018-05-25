#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018


from statux.thermald import *

print("Package Temp: %.2fC°" % x86_pkg_temp())

cores = cores_temp()
for i in range(len(cores)):
    print("Core %d Temp.: %.2fC°" % (i+1, cores[i]))

s = "CPU Temp....: "
print("%s%.2fC°" % (s, cpu_temp("celsius")))
print("%s%.2fF°" % (s, cpu_temp("fahrenheit")))
print("%s%.2fK°" % (s, cpu_temp("kelvin")))
print("%s%.2fR°" % (s, cpu_temp("rankine")))
