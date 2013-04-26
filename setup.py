#!/usr/bin/env python

from glob import glob

from setuptools import setup, find_packages


setup(
    name="proxmox",
    version="1.0.1",
    description="Python API for ProxMox VE 2.0 API",
    packages=find_packages(),
    scripts=glob("scripts/*")
)
