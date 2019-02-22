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

from statux.net import *
from time import sleep
from threading import Thread

interfaces = get_interfaces()

for interface in interfaces:
    print("\n%s: " % interface)
    print("Download : %s" % download_bytes(interface, "auto"))
    print("Upload...: %s" % upload_bytes(interface, "auto"))


def speed(interface_):
    print("%s:" % interface_.ljust(8, "."), down_up_speed(interface_, 0.0, "auto"))


count = 0
threads = []
print("\nDownload, Upload speed:")
while count <= 10:
    for i in range(len(interfaces)):
        t = Thread(args=(interfaces[i], ), target=speed)
        threads.append(t)
        t.start()
    sleep(1)
    count += 1
    print("")
