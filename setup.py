#!/usr/bin/env python

from setuptools import setup

import stacked

setup(name="stacked",
      version=stacked.__version__,
      description="Stacking utilities",
      license="MIT",
      keywords="context stack",
      author="Ischium",
      author_email="support@ischium.net",
      url="https://github.com/ischium/stacked",
      packages=("stacked",),
      tests_require=("nose", "yanc"),
      test_suite="nose.collector",
      )
