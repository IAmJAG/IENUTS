from threading import RLock
from typing import Any, Callable

from .__property import Property, _ValueType


class TSProperty(Property):
    def __init__(self, fget = None, fset = None, fdel = None, doc = None, lock = None):
        super().__init__(fget, fset, fdel, doc)
        self._lock: RLock = RLock() if lock is None else lock

    def _get(self, instance: Any) -> _ValueType:
        with self._lock:
            return super()._get(instance)

    def _set(self, instance, value: _ValueType):
        with self._lock:
            super()._set(instance, value)

    def Getter(self, fget: Callable[[Any], _ValueType]) -> 'TSProperty':
        return TSProperty(
            fget=fget,
            fset=self.fset,
            fdel=self.fdel,
            doc=self.__doc__,
            lock=self._lock
        )

    def Setter(self, fset: Callable[[Any, _ValueType], None]) -> 'TSProperty':
        return TSProperty(
            fget=self.fget,
            fset=fset,
            fdel=self.fdel,
            doc=self.__doc__,
            lock=self._lock
        )

    def Deleter(self, fdel: Callable[[Any], None]) -> 'TSProperty':
        return TSProperty(
            fget=self.fget,
            fset=self.fset,
            fdel=fdel,
            doc=self.__doc__,
            lock=self._lock
        )
