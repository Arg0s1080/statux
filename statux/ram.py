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


from statux._conversions import set_bytes

_STAT_PATH = "/proc/meminfo"


def _get_val(*items) -> list:
    with open(_STAT_PATH, "rb") as file:
        stat_ = file.readlines()
        values = []
        for l in range(len(stat_)):
            for i in range(len(items)):
                if stat_[l].startswith(items[i]):
                    values.insert(i, int(stat_[l].split()[-2]))
            if len(values) == len(items):
                break
        return values


def get_mem_total(scale="MiB", precision=2):
    return set_bytes(_get_val(b"MemTotal")[0], scale_out=scale, precision=precision)


def get_mem_free(scale="MiB", precision=2):
    return set_bytes(_get_val(b"MemFree")[0], scale_out=scale, precision=precision)


def get_mem_free_percent(precision=2) -> float:
    values = _get_val(b"MemFree", b"MemTotal")
    return round(values[0] / values[1] * 100, precision)


def get_mem_available(scale="MiB", precision=2):
    return set_bytes(_get_val(b"MemAvailable")[0], scale_out=scale, precision=precision)


def get_mem_available_percent(precision=2) -> float:
    values = _get_val(b"MemAvailable", b"MemTotal")
    return round(values[0] / values[1] * 100, precision)


def get_mem_buff_cache(scale="MiB", precision=2):
    items = (b"Buffers", b"Cached", b"SReclaimable", b"SUnreclaim")
    buff, cache, sre, sur = map(float, _get_val(*items))
    return set_bytes(buff + cache + sre + sur, scale_out=scale, precision=precision)


def get_mem_used(scale="MiB", precision=2):
    items = (b"MemTotal", b"MemFree", b"Buffers", b"Cached", b"Slab")
    tot, free, buff, cache, slab = map(float, _get_val(*items))
    return set_bytes(tot - (buff + cache + slab + free), scale_out=scale, precision=precision)


def get_mem_used_percent(precision=2):
    items = (b"MemTotal", b"MemFree", b"Buffers", b"Cached", b"Slab")
    tot, free, buff, cache, slab = map(float, _get_val(*items))
    return round((tot - buff - cache - slab - free) / tot * 100, precision)

