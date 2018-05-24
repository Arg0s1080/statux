from statux.disks import *
from time import sleep
from random import choice

partitions = sorted(mounted_partitions().keys())

for ptt in partitions:
    print("\n%s" % ptt)
    print("Used: ", used_space(ptt, "auto"))
    print("Free: ", free_space(ptt, "auto"))
    print("Total:", total_size(ptt, "auto"))

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
      str(bytes_read_write(ptt, interval=5, persecond=True, scale="bytes")))
