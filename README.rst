STATUX
======
Statux is a Python library for Linux that provides methods to get hardware
and system information. Useful for monitoring tasks.


Battery
-------
+-----------------------------+------------------------------------+
|         **Method**          |             **Returns**            |
+-----------------------------+------------------------------------+
| ``battery_info()``          | Manufacturer, model and s/n        |
+-----------------------------+------------------------------------+
| ``status()``                | Full, Charging or Discharging      |
+-----------------------------+------------------------------------+
| ``is_present()``            | True if battery is present         |
+-----------------------------+------------------------------------+
| ``voltage()``               | battery voltage (mV)               |
+-----------------------------+------------------------------------+
| ``current()``               | battery current (mA)               |
+-----------------------------+------------------------------------+
| ``energy()``                | battery energy (mWh)               |
+-----------------------------+------------------------------------+
| ``power()``                 | battery power (mW)                 |
+-----------------------------+------------------------------------+
| ``charge()``                | battery charge (mAh)               |
+-----------------------------+------------------------------------+
| ``capacity()``              | current capacity percent           |
+-----------------------------+------------------------------------+
| ``capacity_level()``        | Full, Normal, Low or Critical      |
+-----------------------------+------------------------------------+
| ``low_level()``             | value set for low battery level    |
+-----------------------------+------------------------------------+
| ``critical_level()``        | value set for critical level       |
+-----------------------------+------------------------------------+
| ``action_level()``          | value set for critical action      |
+-----------------------------+------------------------------------+
| ``critical_power_action()`` | PowerOff, Hibernate or HybridSleep |
+-----------------------------+------------------------------------+
| ``remaining_time()``        | Remaining battery life             |
+-----------------------------+------------------------------------+
| ``wear_level()``            | Battery health level               |
+-----------------------------+------------------------------------+
| ``technology()``            | Chemistry of battery               |
+-----------------------------+------------------------------------+
| ``supply_type()``           | Battery, Mains, UPS, etc           |
+-----------------------------+------------------------------------+
| ``lid_state()``             | Open or Close                      |
+-----------------------------+------------------------------------+
| ``ac_adapter_online()``     | True if AC adapter is online       |
+-----------------------------+------------------------------------+

CPU
---
+-------------------------+----------------------------------+
|        **Method**       |           **Returns**            |
+-------------------------+----------------------------------+
| ``next_value()``        | CPU Load percentage. Note: Needs |
|                         | to instantiate ``Load()`` class  |
+-------------------------+----------------------------------+
| ``logical_cpus()``      | Number of logical processors     |
+-------------------------+----------------------------------+
| ``physical_cpus()``     | Number of physical processor     |
+-------------------------+----------------------------------+
| ``frequency()``         | Current CPU frequency            |
+-------------------------+----------------------------------+
| ``max_frequency()``     | CPU max frequency                |
+-------------------------+----------------------------------+
| ``frequency_percent()`` | Current CPU frequency percent    |
+-------------------------+----------------------------------+
| ``is_x86_64()``         | True if CPU is AMD64 or Intel64  |
|                         | i.e. 64 bit capable              |
+-------------------------+----------------------------------+
| ``model_name()``        | CPU model name                   |
+-------------------------+----------------------------------+

DISKS
-----
+------------------------------+---------------------------------------------+
|         **Method**           |                 **Returns**                 |
+------------------------------+---------------------------------------------+
| ``block_devices()``          | sda, sdb, nvmen1, hda, hdb, etc             |
+------------------------------+---------------------------------------------+
| ``partitions()``             | sda1,sda2, sdb1, nvmen1p1, hda1, hdb2, etc  |
+------------------------------+---------------------------------------------+
| ``is_rotational()``          | If block device is rotational               |
+------------------------------+---------------------------------------------+
| ``is_removable()``           | If block device is removable                |
+------------------------------+---------------------------------------------+
| ``model()``                  | Model name of the given device (sda, hdb..) |
+------------------------------+---------------------------------------------+
| ``disk_naming()``            | a namedtuple with persistent names of a     |
|                              | disk or a partition (id, label, path, uuid  |
|                              | partlabel and partuuid)                     |
+------------------------------+---------------------------------------------+
| ``mounts_info()``            | A dict with mounted partitions as key and a |
|                              | namedtuple with mount point, filesystem and |
|                              | mount options as value                      |
+------------------------------+---------------------------------------------+
| ``mounted_partitions()``     | mounted partitions and mount points         |
+------------------------------+---------------------------------------------+
| ``total_size()``             | Total size of a partition                   |
+------------------------------+---------------------------------------------+
| ``free_space()``             | Free space of a partition                   |
+------------------------------+---------------------------------------------+
| ``used_space()``             | Used space of a partition                   |
+------------------------------+---------------------------------------------+
| ``used_space_percent()``     | Used space percent of a partition           |
+------------------------------+---------------------------------------------+
| ``bytes_read()``             | Bytes read in a partition                   |
+------------------------------+---------------------------------------------+
| ``bytes_write()``            | Bytes written in a partition                |
+------------------------------+---------------------------------------------+
| ``bytes_read_write()``       | Bytes read and wirtten in a partition       |
+------------------------------+---------------------------------------------+
| ``bytes_read_write_multi()`` | Bytes read and writen in several partitions |
+------------------------------+---------------------------------------------+


NETWORK
-------
+----------------------+------------------------------------------+
|      **Method**      |                **Returns**               |
+----------------------+------------------------------------------+
| ``get_interfaces()`` | All network interfaces                   |
+----------------------+------------------------------------------+
| ``get_address()``    | MAC address os a interface               |
+----------------------+------------------------------------------+
| ``get_state()``      | Operational state of a interface         |
+----------------------+------------------------------------------+
| ``download_bytes()`` | total bytes downloaded in a interface    |
+----------------------+------------------------------------------+
| ``upload_bytes()``   | total bytes uploaded in a interface      |
+----------------------+------------------------------------------+
| ``down_up_bytes()``  | total bytes up-downloaded in a interface |
+----------------------+------------------------------------------+
| ``download_bytes()`` | average download speed per second        |
+----------------------+------------------------------------------+
| ``upload_speed()``   | average download speed per second        |
+----------------------+------------------------------------------+
| ``down_up_speed()``  | average up-download speed per second     |
+----------------------+------------------------------------------+

RAM
---
+-------------------------+--------------------------------+
|        **Method**       |           **Returns**          |
+-------------------------+--------------------------------+
| ``total()``             | Total RAM size                 |
+-------------------------+--------------------------------+
| ``free()``              | Free RAM                       |
+-------------------------+--------------------------------+
| ``free_percent()``      | Free RAM percent               |
+-------------------------+--------------------------------+
| ``available()``         | Available RAM                  |
+-------------------------+--------------------------------+
| ``available_percent()`` | Available RAM percent          |
+-------------------------+--------------------------------+
| ``buff_cache()``        | Buffer, cached and slab memory |
+-------------------------+--------------------------------+
| ``used()``              | Used RAM                       |
+-------------------------+--------------------------------+
| ``used_percent()``      | Used RAM percent               |
+-------------------------+--------------------------------+

SYSTEM
------
+---------------------------+-------------------------------------+
|         **Method**        |             **Returns**             |
+---------------------------+-------------------------------------+
| ``boot_time()``           | Time at which the system booted     |
+---------------------------+-------------------------------------+
| ``uptime()``              | Time elapsed since system boot time |
+---------------------------+-------------------------------------+
| ``init()``                | Init system name                    |
+---------------------------+-------------------------------------+
| ``hostame()``             | Hostname                            |
+---------------------------+-------------------------------------+
| ``user()``                | User name                           |
+---------------------------+-------------------------------------+
| ``display_protocol()``    | Display protocol (x11 or wayland)   |
+---------------------------+-------------------------------------+
| ``kernel_release()``      | Kernel release                      |
+---------------------------+-------------------------------------+
| ``kernel version()``      | Kernel version                      |
+---------------------------+-------------------------------------+
| ``architecture()``        | Machine type                        |
+---------------------------+-------------------------------------+
| ``session_id()``          | Current session id                  |
+---------------------------+-------------------------------------+
| ``distro_name()``         | Distro short name                   |
+---------------------------+-------------------------------------+
| ``distro_full_name()``    | Full distro description             |
+---------------------------+-------------------------------------+
| ``distro_version()``      | Distro version                      |
+---------------------------+-------------------------------------+
| ``distro_url()``          | Distro url                          |
+---------------------------+-------------------------------------+
| ``linux_distribution()``  | Distro info (id, version, codename) |
+---------------------------+-------------------------------------+

TEMP
----
+---------------+---------------------------------------------+
|   **Method**  |                  **Returns**                |
+---------------+---------------------------------------------+
| ``cores()``   | temperature of each core                    |
+---------------+---------------------------------------------+
| ``cpu()``     | CPU temp                                    |
+---------------+---------------------------------------------+
| ``max_val()`` | maximum value of the temp sensors obtained  |
+---------------+---------------------------------------------+

Note:
^^^^^
These methods are based on the proc and sys filesystems and are tested in **Linux 4.15**.
It is possible that some methods are not available in previous kernel versions

Install:
--------

By pip (It may not be the latest version):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    pip install statux

Cloning this repo :
^^^^^^^^^^^^^^^^^^^

::

    git clone https://github.com/Arg0s1080/statux.git
    cd statux
    sudo python3 setup.py install

