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

from types import TracebackType
from typing import Optional, Type
from typing_extensions import Literal, Self
from .abstract_base import AbstractBase, abstractmethod


class AbstractContextManager(object, metaclass=AbstractBase):
    """
    Closable class that supports being used as a simple context manager.
    """

    __slots__ = ()

    @abstractmethod
    def close(self) -> None:
        """
        How to actually close the underlying resources.
        """

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Optional[Type], exc_val: Exception,
                 exc_tb: TracebackType) -> Literal[False]:
        self.close()
        return False