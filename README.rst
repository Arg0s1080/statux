STATUX
======
Statux is a Python library for Linux that provides methods to get hardware
and system information. Useful for monitoring tasks.


Battery
-------
+-----------------------+------------------------------------+
|         Method        |               Returns              |
+-----------------------+------------------------------------+
| battery               | Manufacturer, model and s/n        |
+-----------------------+------------------------------------+
| status                | Full, Charging or Discharging      |
+-----------------------+------------------------------------+
| is_present            | True if battery is present         |
+-----------------------+------------------------------------+
| voltage               | battery voltage (mV)               |
+-----------------------+------------------------------------+
| current               | battery current (mA)               |
+-----------------------+------------------------------------+
| power                 | battery power (mW)                 |
+-----------------------+------------------------------------+
| charge                | battery charge (mAh)               |
+-----------------------+------------------------------------+
| capacity              | current capacity percent           |
+-----------------------+------------------------------------+
| capacity_level        | Full, Normal, Low or Critical      |
+-----------------------+------------------------------------+
| low_level             | value set for low battery level    |
+-----------------------+------------------------------------+
| critical_level        | value set for critical level       |
+-----------------------+------------------------------------+
| critical_power_action | PowerOff, Hibernate or HybridSleep |
+-----------------------+------------------------------------+
| remaining_time        | Remaining battery life             |
+-----------------------+------------------------------------+
| wear_level            | Battery health level               |
+-----------------------+------------------------------------+
| technology            | Chemistry of battery               |
+-----------------------+------------------------------------+
| supply_type           | Battery, Mains, UPS, etc           |
+-----------------------+------------------------------------+
| lid_state             | Open or Close                      |
+-----------------------+------------------------------------+
| ac_adapter_online     | True if AC adapter is online       |
+-----------------------+------------------------------------+

CPU
---
+-------------------+-------------------------------+
|       Method      |            Returns            |
+-------------------+-------------------------------+
| logical_cpus      | Number of logical processors  |
+-------------------+-------------------------------+
| physical_cpus     | Number of physical processor  |
+-------------------+-------------------------------+
| load_percent      | CPU load percentage           |
+-------------------+-------------------------------+
| frequency         | Current CPU frequency         |
+-------------------+-------------------------------+
| max_frequency     | CPU max frequency             |
+-------------------+-------------------------------+
| frequency_percent | Current CPU frequency percent |
+-------------------+-------------------------------+
| is_64_bit         | True if CPU is 64 bits        |
+-------------------+-------------------------------+


DISKS
-----
+------------------------+---------------------------------------------+
|         Method         |                   Returns                   |
+------------------------+---------------------------------------------+
| partitions             | sda1,sda2, sdb1, etc                        |
+------------------------+---------------------------------------------+
| is_rotational          | If block device is rotational               |
+------------------------+---------------------------------------------+
| is_removable           | If block device is removable                |
+------------------------+---------------------------------------------+
| mounted_partitions     | mounted partitions and mount points         |
+------------------------+---------------------------------------------+
| total_size             | Total size of a partition                   |
+------------------------+---------------------------------------------+
| free_space             | Free space of a partition                   |
+------------------------+---------------------------------------------+
| used_space             | Used space of a partition                   |
+------------------------+---------------------------------------------+
| used_space_percent     | Used space percent of a partition           |
+------------------------+---------------------------------------------+
| bytes_read             | Bytes read in a partition                   |
+------------------------+---------------------------------------------+
| bytes_write            | Bytes written in a partition                |
+------------------------+---------------------------------------------+
| bytes_read_write       | Bytes read and wirtten in a partition       |
+------------------------+---------------------------------------------+
| bytes_read_write_multi | Bytes read and writen in several partitions |
+------------------------+---------------------------------------------+


NETWORK
-------
+----------------+------------------------------------------+
|     Method     |                  Returns                 |
+----------------+------------------------------------------+
| get_interfaces | All network interfaces                   |
+----------------+------------------------------------------+
| download_bytes | total bytes downloaded in a interface    |
+----------------+------------------------------------------+
| upload_bytes   | total bytes uploaded in a interface      |
+----------------+------------------------------------------+
| down_up_bytes  | total bytes up-downloaded in a interface |
+----------------+------------------------------------------+
| download_bytes | average download speed per second        |
+----------------+------------------------------------------+
| upload_speed   | average download speed per second        |
+----------------+------------------------------------------+

RAM
---
+--------------+--------------------------------+
|    Method    |             Returns            |
+--------------+--------------------------------+
| total        | Total RAM size                 |
+--------------+--------------------------------+
| free         | Free RAM                       |
+--------------+--------------------------------+
| free_percent | Free RAM percent               |
+--------------+--------------------------------+
| available    | Available RAM percent          |
+--------------+--------------------------------+
| buff_cache   | Buffer, cached and slab memory |
+--------------+--------------------------------+
| used         | Used RAM                       |
+--------------+--------------------------------+
| used_percent | Used RAM percent               |
+--------------+--------------------------------+

SYSTEM
------
+---------------------+-------------------------------------+
|        Method       |               Returns               |
+---------------------+-------------------------------------+
| boot_time           | Time at which the system booted     |
+---------------------+-------------------------------------+
| uptime              | Time elapsed since system boot time |
+---------------------+-------------------------------------+
| init                | Init system name                    |
+---------------------+-------------------------------------+
| hostame             | Hostname                            |
+---------------------+-------------------------------------+
| kernel_release      | Kernel release                      |
+---------------------+-------------------------------------+
| kernel version      | Kernel version                      |
+---------------------+-------------------------------------+
| system_architecture | Machine type                        |
+---------------------+-------------------------------------+

TEMP
----
+---------+----------------------------------------+
|  Method |                 Returns                |
+---------+----------------------------------------+
| x86_pkg | temperature package level sensor value |
+---------+----------------------------------------+
| cores   | temperature of each core               |
+---------+----------------------------------------+
| cpu     | CPU temp                               |
+---------+----------------------------------------+

Note:
^^^^^
These methods are based on the proc and sys filesystems and are tested in **Linux 4.15**.
It is possible that some methods are not available in previous kernel versions

Install:
--------

::

    pip install statux

