from statux.cpu import *
from examples.functions import *


print_txt("Boot time", boot_time(str_format=True))
print_txt("Boot time", boot_time(), "seconds")
print_txt("Uptime", uptime(str_format=True))
print_txt("Physical CPU's", physical_cpus())
print_txt("Logical CPU's", logical_cpus())
print_txt("Max Frequency", cpu_max_frequency(False, scale="ghz"), "GHz")

print("\nCPU Load (interval > 0):")
stat = cpu_load(interval=1.0, per_core=True, precision=1)
for cpu in range(len(stat)):
    print("cpu%d: %.1f%%" % (cpu + 1, stat[cpu]))


print("\nCPU Load (interval == 0):")
count = 0
while count <= 10:
    print_txt("Current CPU Load", cpu_load(0.0, False), "%")
    sleep(1)
    count += 1

print("\nCPU Frequency:")
freq = cpu_frequency()
freq_percent = cpu_frequency_percent()

while count > 0:
    for cpu in range(logical_cpus()):
        print("Frequency cpu%d: %.3f MHz (%.2f%%)" % (cpu+1, freq[cpu], freq_percent[cpu]))
    print("")
    sleep(1)
    count -= 1
