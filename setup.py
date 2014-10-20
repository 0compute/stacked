#!/usr/bin/env python

# Copyright 2012-2014 Arthur Noel
#
# This file is part of Stacked.
#
# Stacked is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Stacked is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Stacked. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from setuptools.command import test

# monkey patch test command to make nose work with `setup.py test`
# see: http://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-python-setuptools-test-command/
test._test = test.test


class NoseTestCommand(test._test):

    user_options = test._test.user_options + [
        ("args=", "a", "Arguments to pass to nose"),
    ]

    def initialize_options(self):
        test._test.initialize_options(self)
        self.args = None

    def finalize_options(self):
        test._test.finalize_options(self)
        self.args = self.args and self.args.strip().split() or []
        self.test_suite = True

    def run_tests(self):
        import nose
        nose.run_exit(argv=["nosetests"] + self.args)

test.test = NoseTestCommand


setup(
    setup_requires=["pbr"],
    pbr=True,
    tests_require=[
        "nose >= 1.3",
        "yanc >= 0.2",
    ],
    test_suite="nose.collector",
)
