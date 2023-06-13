# Copyright (c) 2017 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict
from collections.abc import MutableSet
from typing import (
    Any, Dict, Set, Iterable, Iterator, Optional, Generic, TypeVar)

T = TypeVar("T")


class OrderedSet(MutableSet[T], Generic[T]):
    __slots__ = (
        "_map",
    )

    def __init__(self, iterable: Optional[Set[T]] = None):
        # pylint: disable=super-init-not-called
        # Always use OrderedDict as plain dict does not support
        # __reversed__ and key indexing
        self._map: Dict[T, None] = OrderedDict()

        # or is overridden in mutable set; calls add on each element
        if iterable is not None:
            self |= iterable

    def add(self, value: T):
        if value not in self._map:
            self._map[value] = None

    def discard(self, value: T):
        if value in self._map:
            self._map.pop(value)

    def __iter__(self) -> Iterator[T]:
        return self._map.__iter__()

    def __reversed__(self) -> Iterator[T]:
        return self._map.__reversed__()

    def peek(self, last: bool = True) -> T:
        if not self._map:  # i.e., is self._map empty?
            raise KeyError('set is empty')
        if last:
            return next(reversed(self))
        else:
            return next(iter(self))

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: Any) -> bool:
        return key in self._map

    def update(self, iterable: Iterable[T]):
        for item in iterable:
            self.add(item)

    def pop(self, last: bool = True) -> T:  # pylint: disable=arguments-differ
        key = self.peek(last)
        self.discard(key)
        return key

    def __repr__(self) -> str:
        if not self._map:  # i.e., is self._map empty?
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and self._map == other._map
        return set(self) == set(other)

    def __ne__(self, other: Any) -> bool:
        """
        Comparison method for comparing ordered sets.

        :param other: instance of OrderedSet
        :rtype: None
        """
        return not self.__eq__(other)
