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

from statux.disks import *
from time import sleep
from random import choice

print("Block ", "Rotational", "Removable")
for block in sorted(block_devices()):
    print(block.center(6),  str(is_rotational(block)).center(10), str(is_removable(block)).center(9))

ptt_dict = mounted_partitions()
print("\nPartition", "Mount point")
for key in sorted(ptt_dict, key=ptt_dict.__getitem__):
    print(key.center(9), ptt_dict[key])

partitions = sorted(ptt_dict.keys())

for ptt in partitions:
    print("\n%s" % ptt)
    print("Used :", used_space(ptt, "auto"))
    print("Free :", free_space(ptt, "auto"))
    print("Total:", total_size(ptt, "auto"))

print()
count = 0
while count <= 10:
    stat = bytes_read_write_multi(*partitions, scale="auto")
    for partition, values in stat.items():
        print("%s: %s - %s" % (partition, values[0], values[1]))
    sleep(1)
    count += 1
    print("")

ptt = choice(partitions)
print("\n%s STAT.\nSleeping 3 seconds..." % ptt.upper())
print("Total KiB read: %.2f" % bytes_read(ptt, 3.0))


ptt = choice(partitions)
print("\n%s STAT.\nSleeping 5 seconds..." % ptt.upper())
print("Average bytes per second (read, write): %s" %
      str(bytes_read_write(ptt, interval=5, per_second=True, scale="bytes")))
