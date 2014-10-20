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

import copy


class Stacked(object):

    def __init__(self):
        self._entered = False
        self._push_stack = []
        self._patch_stack = []
        self._to_push = []
        self._to_push_member = []
        self._to_patch = []

    def _patch_target(self, target, member, patch):
        if isinstance(target, dict):
            target[member] = patch
        else:
            setattr(target, member, patch)

    def _patch(self, target, member, patch):
        if isinstance(target, dict):
            current = target[member]
        else:
            current = getattr(target, member, None)
            if isinstance(current, dict) and isinstance(patch, dict):
                # if we are patching a dictionary we want to update not replace
                tmp = copy.copy(current)
                tmp.update(patch)
                patch = tmp
        self._patch_target(target, member, patch)
        self._patch_stack.append((target, member, current))

    def register_patch(self, target, member, patch):
        self._to_patch.append((target, member, patch))

    def _push(self, obj):
        self._push_stack.append(obj)
        obj.__enter__()

    def register_push(self, obj):
        self._to_push.append(obj)

    def register_push_member(self, name, obj):
        setattr(self, name, obj)
        self._to_push_member.append(name)

    def __enter__(self):
        if self._entered:
            raise RuntimeError("Can't reenter %r " % self)
        self._entered = True
        for patch in self._to_patch:
            self._patch(*patch)
        for obj in self._to_push:
            self._push(obj)
        for name in self._to_push_member:
            self._push(getattr(self, name))
        return self

    def __exit__(self, etype, evalue, etraceback):
        if not self._entered:
            raise RuntimeError("Haven't entered %r" % self)
        while self._push_stack:
            obj = self._push_stack.pop()
            obj.__exit__(etype, evalue, etraceback)
        while self._patch_stack:
            target, member, patch = self._patch_stack.pop()
            self._patch_target(target, member, patch)
        self._entered = False

    # for convenience when not using as a context manager
    push = __enter__
    pop = __exit__
