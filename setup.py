#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from telestatsd import __version__


setup(name='telestatsd',
      version=__version__,
      description=('StatsD client in Python with support for Telegraf '
                   'and SRV records in DNS'),
      author='Opera Wrocław Services',
      author_email='svc-code@opera.com',
      url='https://github.com/operasoftware/telestatsd/',
      license='MIT',
      keywords='statsd telegraf srv service record',
      download_url=('https://github.com/operasoftware/telestatsd/tarball/' +
                    __version__),
      packages=find_packages(),
      install_requires=['srvlookup==0.2.0'],
      zip_safe=False)
