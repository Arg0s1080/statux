#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018


from statux.temp import *

print("Package Temp: %.2fC°" % x86_pkg())

cores = cores()
for i in range(len(cores)):
    print("Core %d Temp.: %.2fC°" % (i+1, cores[i]))

s = "CPU Temp....: "
print("%s%.2fC°" % (s, cpu("celsius")))
print("%s%.2fF°" % (s, cpu("fahrenheit")))
print("%s%.2fK°" % (s, cpu("kelvin")))
print("%s%.2fR°" % (s, cpu("rankine")))
