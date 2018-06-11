#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0
#
# Permissions of this strong copyleft license are conditioned on making available
# complete source code of licensed works and modifications, which include larger works
# using a licensed work, under the same license. Copyright and license notices must be
# preserved. Contributors provide an express grant of patent rights.
#
# For more information on this, and how to apply and follow theGNU GPL, see:
# http://www.gnu.org/licenses
#
# (ɔ) Iván Rincón 2018


from os import statvfs
from os import listdir
from statux._conversions import set_bytes

_STAT = "/proc/"
_DEV = "/dev/"
_BLOCK_DEV = "/sys/block/"
_QUEUE = "/queue/"
_LB_SIZE = "%slogical_block_size" % _QUEUE
_PB_SIZE = "%sphysical_block_size" % _QUEUE
_MOUNTS = "%smounts" % _STAT
_PARTITIONS = "%spartitions" % _STAT
_DISKSTATS = "%sdiskstats" % _STAT
_last = None


def block_devices() -> list:
    """Returns a list with block devices (HDD, SSD, pendrives, micro-sd, DVD, etc)"""
    return [block for block in listdir(_BLOCK_DEV)]


def partitions() -> list:
    """Returns a list with partitions"""
    with open(_PARTITIONS, "r") as f:
        stat = f.readlines()
        res = []
        dsk = block_devices()
        for i in range(2, len(stat)):
            ptt = stat[i].split()[3]
            if ptt not in dsk:
                res.append(ptt)
    return res


def _check_partitions(*partitions_):
    valid_partitions = partitions()
    for ptt in partitions_:
        if ptt not in valid_partitions:
            raise ValueError("%s is not a valid partition" % ptt)


def _check_block(block):
    if block not in block_devices():
        raise ValueError("%s is not a valid block device" % block)
    return block


def is_rotational(block_device: str) -> bool:
    """Returns True if the device is of rotational type, False otherwise"""
    with open("%s%s%s%s" % (_BLOCK_DEV, _check_block(block_device), _QUEUE, "rotational"), "rb") as f:
        return bool(int(f.read()))


def is_removable(block_device: str) -> bool:
    """Returns True is the device is removable, False otherwise"""
    with open("%s%s%s" % (_BLOCK_DEV, _check_block(block_device), "/removable"), "rb") as f:
        return bool(int(f.read()))


def mounted_partitions() -> dict:
    """Returns a dict with mounted partitions and mount points"""
    def get_mounts():
        with open(_MOUNTS, "r") as file:
            return {line.split()[0]: line.split()[1] for line in file.readlines() if line.startswith("/")}
    res = {}
    mounts = get_mounts()
    for partition in partitions():
        dev = "%s%s" % (_DEV, partition)
        if dev in mounts.keys():
            res[partition] = mounts[dev]
    return res


def _get_stat(partition):
    mounts = mounted_partitions()
    try:
        return statvfs(mounts[partition])
    except KeyError:
        raise ValueError("Partition not mount")


def _get_disks_stats():
    # Returns sectors read/written * f_frsize
    def get_bs(ptt, logical):
        for dev in listdir(_BLOCK_DEV):
            if dev in ptt:
                with open("%s%s%s" % (_BLOCK_DEV, dev, _LB_SIZE if logical else _PB_SIZE), "rb") as fl:
                    return int(fl.read())
    res = {}
    with open(_DISKSTATS, "r") as f:
        stat = f.readlines()
        for line in stat:
            ln = line.split()
            partition = ln[2]
            bsize = get_bs(partition, True)  # logical block size
            res[str(partition)] = int(ln[5]) * bsize, int(ln[9]) * bsize
    return res


def total_size(partition: str, scale="GiB", precision=2):
    """Returns total size of a partition

    :Params:
        :partition (str): Partition name (Ex: 'sda1')
        :scale     (str): Return scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
                         GiB by default.
        :precision (int): Number of rounding decimals
    """

    stat = _get_stat(partition)
    return set_bytes(stat.f_frsize * stat.f_blocks, scale_in="bytes", scale_out=scale, precision=precision)


def free_space(partition: str, scale="GiB", precision=2):
    """Returns free partition space

        :Params:
            :partition (str): Partition name (Ex: 'sda1')
            :scale     (str): Return scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
            :precision (int): Number of rounding decimals
        """

    stat = _get_stat(partition)
    return set_bytes(stat.f_frsize * stat.f_bavail, scale_in="bytes", scale_out=scale, precision=precision)


def used_space(partition: str, scale="GiB", precision=2):
    """Returns used partition space

        :Params:
            :partition (str): Partition name (Ex: 'sda1')
            :scale     (str): Return scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
                             GiB by default
            :precision (int): Number of rounding decimals
        """

    stat = _get_stat(partition)
    return set_bytes((stat.f_blocks - stat.f_bfree) * stat.f_frsize,
                     scale_in="bytes", scale_out=scale, precision=precision)


def used_space_percent(partition: str, precision=2) -> float:
    """Returns used partition space percentage

        :Params:
            :partition (str): Partition name (Ex: 'sda1')
            :precision (int): Number of rounding decimals
        """

    stat = _get_stat(partition)
    return round((stat.f_blocks - stat.f_bfree) / stat.f_blocks * 100, precision)


def _set_delta(*partitions_: str, interval=0.0, persecond=False):
    from time import sleep, time
    global _last
    if _last is None or interval > 0.0:
        _check_partitions(*partitions_)
        old_stat = _get_disks_stats()
        sleep(interval)
        elapsed = interval
    else:
        old_stat = _last[0]
        elapsed = round(time() - _last[1], 3)  # milliseconds
    new_stat = _get_disks_stats()
    _last = new_stat, time()
    f = {}
    for partition in partitions_:
        read_delta = new_stat[partition][0] - old_stat[partition][0]
        write_delta = new_stat[partition][1] - old_stat[partition][1]
        res = ((read_delta, write_delta) if not persecond else (0.0, 0.0) if not elapsed else
               (read_delta / elapsed, write_delta / elapsed))
        if len(partitions_) < 2:
            return res
        else:
            f[partition] = res
    return f


def bytes_read(partition: str, interval=0.0, per_second=False, scale="KiB", precision=2):
    """Returns bytes read in a partition in a certain time interval

        :Params:
            :partition  (str):  Partition name (Ex: 'sda1')
            :interval (float):  Seconds. When value is greater than zero, it returns bytes read
                                in that period of time. When interval value is 0, it returns
                                bytes read since the last call
            :per_second (bool): If it's True returns average value per second
            :scale      (str):  Output scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
                                KiB by default
            :precision  (int):  Number of rounding decimal
    """

    return set_bytes(_set_delta(partition, interval=interval, persecond=per_second)[0],
                     scale_in="bytes", scale_out=scale, precision=precision)


def bytes_write(partition: str, interval=0.0, per_second=False, scale="KiB", precision=2):
    """Returns written bytes in a partition in a certain time interval

        :Params:
            :partition  (str):  Partition name (Ex: 'sda1')
            :interval (float):  Seconds. When value is greater than zero, it returns bytes written
                                in that period of time. When interval value is 0, it returns
                                bytes read since the last call
            :per_second (bool): If it's True returns average value per second
            :scale      (str):  Output scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
                                KiB by default
            :precision  (int):  Number of rounding decimal
    """

    return set_bytes(_set_delta(partition, interval=interval, persecond=per_second)[1],
                     scale_in="bytes", scale_out=scale, precision=precision)


def bytes_read_write(partition: str, interval=0.0, per_second=False, scale="KiB", precision=2) -> tuple:
    """Returns a tuple with bytes read and written in a partition in a certain time interval

        :Params:
            :partition  (str):  Partition name (Ex: 'sda1')
            :interval (float):  Seconds. When value is greater than zero, it returns bytes read
                                and written in that period of time. When interval value is 0,
                                it returns bytes read and written since the last call
            :per_second (bool): If it's True returns average value per second
            :scale      (str):  Output scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
                                KiB by default
            :precision  (int):  Number of rounding decimal
    """
    values = _set_delta(partition, interval=interval, persecond=per_second)
    return set_bytes(values[0], values[1], scale_in="bytes", scale_out=scale, precision=precision)


def bytes_read_write_multi(*partitions_: str, interval=0.0, per_second=False, scale="KiB", precision=2) -> dict:
    """Returns a dictionary with the bytes read and written in the given partitions.

        :Params:
            :partitions (str):  Partitions names (Ex: 'sda1','sda2','sda7')
            :interval (float):  Seconds. When value is greater than zero, it returns bytes read
                                and written in that period of time. When interval value is 0,
                                it returns bytes read and written since the last call
            :per_second (bool): If it's True returns average value per second
            :scale      (str):  Output scale (bytes, KiB, MiB, GiB, TiB, kB, MB, TB or auto)
                                KiB by default
            :precision  (int):  Number of rounding decimal
    """
    dic = _set_delta(*partitions_, interval=interval, persecond=per_second)
    if type(dic) == tuple:
        dic = {partitions_[0]: dic}
    for key, value in dic.items():
        dic[key] = set_bytes(value[0], value[1], scale_in="bytes", scale_out=scale, precision=precision)
    return dic
