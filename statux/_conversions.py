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

from statux._errors import UnsupportedScaleError


def set_bytes(*values, scale_in="KiB", scale_out="MiB", precision=2):
    # Function returns: int if scale_out == 'bytes', str if scale_out == 'auto', float otherwise
    f = []
    auto = True if scale_out == "auto" else False
    for value in values:
        scale_in = scale_in.lower()
        if scale_in == "bytes" or scale_in == "b":
            bytes_ = value
        elif scale_in == "kb":
            bytes_ = value * 10**3
        elif scale_in == "mb":
            bytes_ = value * 10**6
        elif scale_in == "gb":
            bytes_ = value * 10**9
        elif scale_in == "kib":
            bytes_ = value * 2**10
        elif scale_in == "mib":
            bytes_ = value * 2**20
        elif scale_in == "gib":
            bytes_ = value * 2**30
        else:
            raise UnsupportedScaleError(scale_in)
        if auto:
            if bytes_ >= 2**40:
                scale_out = "TiB"
            elif bytes_ >= 2**30:
                scale_out = "GiB"
            elif bytes_ >= 2**20:
                scale_out = "MiB"
            elif bytes_ >= 2**10:
                scale_out = "KiB"
            else:
                scale_out = "bytes"
        if scale_out.lower() == "bytes" or scale_out.lower() == "b":
            r = int(bytes_)
        elif scale_out.lower() == "kb":
            r = bytes_ / 10**3
        elif scale_out.lower() == "mb":
            r = bytes_ / 10**6
        elif scale_out.lower() == "gb":
            r = bytes_ / 10**9
        elif scale_out.lower() == "tb":
            r = bytes_ / 10 ** 12
        elif scale_out.lower() == "kib":
            r = bytes_ / 2**10
        elif scale_out.lower() == "mib":
            r = bytes_ / 2**20
        elif scale_out.lower() == "gib":
            r = bytes_ / 2**30
        elif scale_out.lower() == "tib":
            r = bytes_ / 2**40
        else:
            raise UnsupportedScaleError(scale_out)
        res = round(r, precision) if not auto else "%s %s" % (round(r, precision), scale_out)
        f.append(res)

    return f[0] if len(f) < 2 else tuple(f)


def set_mhz(value: float, scale="mhz"):
    scale = scale.lower()
    if scale == "mhz":
        f = value
    elif scale == "ghz":
        f = value / 1000
    elif scale .lower() == "khz":
        f = value * 1000
    elif scale.lower() == "hz":
        f = value * 10**6
    else:
        raise UnsupportedScaleError(scale)
    return f


def set_celsius(degrees: float, scale: str, precision: int):
    degrees /= 1000
    if scale == "celsius":
        r = degrees
    elif scale == "fahrenheit":
        r = 9.0 / 5.0 * degrees + 32
    elif scale == "kelvin":
        r = degrees + 273.15
    elif scale == "rankine":
        r = 9.0 / 5.0 * degrees + 482.67
    else:
        raise UnsupportedScaleError(scale)
    return round(r, precision)
