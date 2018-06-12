# -*- coding: UTF8 -*-

from setuptools import setup
from os.path import abspath, dirname, join
from statux import __version__

with open(join(abspath(dirname(__file__)), "README.rst"), 'r') as readme:
    long_description = readme.read()

setup(
    name="statux",
    version=__version__,
    description="Python module for hardware and system monitoring",
    license="GPLv3",
    long_description=long_description,
    author='Ivan Rincon',
    author_email='ivan.rincon76@gmail.com',
    url="https://github.com/Arg0s1080/statux",
    keywords="linux stats monitoring sensors proc sys battery cpu disk net ram hardware "
             "cpuinfo diskstats meminfo mounts partitions power_supply thermal temp",
    packages=["statux"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Benchmark",
        "Topic :: System :: Hardware",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Operating System",
        "Topic :: Utilities"

    ]
)
