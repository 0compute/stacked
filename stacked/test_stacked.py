# Copyright 2012-2013 Arthur Noel
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

from __future__ import with_statement  # py25 compat

import unittest

from .stacked import Stacked


class _TestObject(object):
    one = 1
    two = dict(three=3)


class _TestStackedObject(Stacked):
    pass


class TestStacked(unittest.TestCase):

    def test_patch_target(self):
        stacked = Stacked()
        obj = _TestObject()
        stacked._patch_target(obj, "one", 2)
        self.assertEqual(obj.one, 2)
        stacked._patch_target(obj.two, "three", 4)
        self.assertEqual(obj.two["three"], 4)

    def test_patch_std(self):
        stacked = Stacked()
        obj = _TestObject()
        stacked._patch(obj, "one", 2)
        self.assertEqual(obj.one, 2)
        self.assertEqual(stacked._patch_stack, [(obj, "one", 1)])

    def test_patch_dict(self):
        stacked = Stacked()
        obj = _TestObject()
        stacked._patch(obj, "two", dict(four=4))
        self.assertEqual(obj.two, dict(three=3, four=4))
        self.assertEqual(stacked._patch_stack, [(obj, "two", dict(three=3))])

    def test_patch_dict_member(self):
        stacked = Stacked()
        obj = _TestObject()
        stacked._patch(obj.two, "three", 4)
        self.assertEqual(obj.two["three"], 4)
        self.assertEqual(stacked._patch_stack, [(obj.two, "three", 3)])

    def test_register_patch(self):
        stacked = Stacked()
        obj = _TestObject()
        to_patch = [(obj, "one", 2)]
        stacked._register_patch(obj, "one", 2)
        self.assertEqual(obj.one, 1)
        self.assertEqual(stacked._to_patch, to_patch)
        with stacked:
            self.assertEqual(obj.one, 2)
        self.assertEqual(obj.one, 1)

    def test_push(self):
        stacked = Stacked()
        obj = _TestStackedObject()
        stacked._push(obj)
        self.assertTrue(obj._entered)
        self.assertEqual(stacked._push_stack, [obj])

    def test_register_push(self):
        stacked = Stacked()
        obj = _TestStackedObject()
        stacked._register_push(obj)
        self.assertFalse(obj._entered)
        self.assertEqual(stacked._push_stack, [])
        with stacked:
            self.assertTrue(obj._entered)
            self.assertEqual(stacked._push_stack, [obj])
        self.assertFalse(obj._entered)
        self.assertEqual(stacked._push_stack, [])

    def test_register_push_member(self):
        stacked = Stacked()
        obj = _TestStackedObject()
        stacked._register_push_member("obj", obj)
        self.assertEqual(stacked.obj, obj)
        self.assertFalse(obj._entered)
        self.assertEqual(stacked._push_stack, [])
        with stacked:
            self.assertTrue(obj._entered)
            self.assertEqual(stacked._push_stack, [obj])
        self.assertFalse(obj._entered)
        self.assertEqual(stacked._push_stack, [])

    def test_double_entry(self):
        stacked = Stacked()
        stacked.__enter__()
        self.assertRaises(RuntimeError, stacked.__enter__)

    def test_bad_exit(self):
        stacked = Stacked()
        self.assertRaises(RuntimeError, stacked.__exit__, None, None, None)
