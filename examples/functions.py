from time import sleep


def print_txt(description, value, unit="", length=18):
    unit = "" if value is None else unit
    print("%s: %s %s" % ((description + " ").ljust(length, "."), str(value), unit))


def repeat(times, fun, *args, **kwargs):
    for _ in range(times):
        fun(*args, **kwargs)
        sleep(1)

