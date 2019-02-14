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
# (ɔ) Iván Rincón 2019


from statux._conversions import set_bytes
from statux._errors import ValueNotFoundError, ex_handler

_MEMINFO = "/proc/meminfo"


def _get_val(*items) -> list:
    with open(_MEMINFO, "rb") as file:
        values = []
        indices = []
        l_items = len(items)
        for l in file:
            for i, value in enumerate(items):
                if l.startswith(value):
                    values.append(int(l.split()[-2]))
                    indices.append(i)
            if len(values) == l_items:
                break
        if len(values) != l_items:
            nf = [items[k].decode() for k in [j for j in list(range(l_items)) if j not in indices]]
            raise ValueNotFoundError(" ".join(nf), _MEMINFO, 61)
        return values


@ex_handler(_MEMINFO)
def total(scale="MiB", precision=2):
    """Returns total RAM memory size

        :Params:
            :scale     (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, MB, GB, TB or auto)
            :precision (int): Number of rounding decimals

    """
    return set_bytes(_get_val(b"MemTotal")[0], scale_out=scale, precision=precision)


@ex_handler(_MEMINFO)
def free(scale="MiB", precision=2):
    """Returns free RAM

        :Params:
            :scale     (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, MB, GB, TB or auto)
            :precision (int): Number of rounding decimals

    """
    return set_bytes(_get_val(b"MemFree")[0], scale_out=scale, precision=precision)


@ex_handler(_MEMINFO)
def free_percent(precision=2) -> float:
    """Returns free RAM percent

     The amount of memory which is currently not used for anything

        :Params:
            :precision (int): Number of rounding decimals

    """
    values = _get_val(b"MemFree", b"MemTotal")
    return round(values[0] / values[1] * 100, precision)


@ex_handler(_MEMINFO)
def available(scale="MiB", precision=2):
    """Returns available RAM

    The amount of RAM which is available for allocation to a new process or to existing processes

        :Params:
            :scale     (str): Chosen scale (bytes, KiB, MiB, GiB, TiB, kB, MB, GB, TB or auto)
            :precision (int): Number of rounding decimals

        """
    return set_bytes(_get_val(b"MemAvailable")[0], scale_out=scale, precision=precision)


@ex_handler(_MEMINFO)
def available_percent(precision=2) -> float:
    """Returns available RAM percent

    The amount of RAM which is available for allocation to a new process or to existing processes

        :Params:
            :precision (int): Number of rounding decimals

        """
    values = _get_val(b"MemAvailable", b"MemTotal")
    return round(values[0] / values[1] * 100, precision)


@ex_handler(_MEMINFO)
def buff_cache(scale="MiB", precision=2):
    """Returns buffers, cached and slab memory

        :Params:
            :precision (int): Number of rounding decimals
    """
    items = (b"Buffers", b"Cached", b"SReclaimable", b"SUnreclaim")
    buff, cache, sre, sur = map(float, _get_val(*items))
    return set_bytes(buff + cache + sre + sur, scale_out=scale, precision=precision)


@ex_handler(_MEMINFO)
def used(scale="MiB", precision=2):
    """Returns used RAM memory

    Used = Total - (Free + Buffers + Cached + Slab)

        :Params:
            :precision (int): Number of rounding decimals

    """
    items = (b"MemTotal", b"MemFree", b"Buffers", b"Cached", b"Slab")
    tot, free_, buff, cached, slab = map(float, _get_val(*items))
    return set_bytes(tot - (buff + cached + slab + free_), scale_out=scale, precision=precision)


@ex_handler(_MEMINFO)
def used_percent(precision=2):
    """Returns used RAM percentage

        :Params:
            :precision (int): Number of rounding decimals

    """
    items = (b"MemTotal", b"MemFree", b"Buffers", b"Cached", b"Slab")
    tot, free_, buff, cache, slab = map(float, _get_val(*items))
    return round((tot - buff - cache - slab - free_) / tot * 100, precision)
