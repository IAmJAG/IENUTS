from inspect import _empty, signature
from typing import Any, Callable, Optional, TypeVar

from ..types import Is
from ..utilities import default

_ValueType = TypeVar("_ValueType")


class Property(property):
    __slots__ = ("_attributeName", "_key", "_owner", "_type")

    def __init__(
        self,
        fget: Optional[Callable[[Any], _ValueType]] = None,
        fset: Optional[Callable[[Any, _ValueType], None]] = None,
        fdel: Optional[Callable[[Any], None]] = None,
        doc: Optional[str] = None,
    ):
        if not callable(fget):
            raise Exception(
                f"Getter is expected to be a method, got {type(fget).__name__}"
            )

        lSignature = signature(fget)
        lReturnType = lSignature.return_annotation

        if lReturnType == _empty or lReturnType == Any or lReturnType is None:
            raise TypeError(
                f"Getter requires explicit return type, got {lReturnType.__name__} instead."
            )

        if fset is not None:
            if not callable(fset):
                raise TypeError(
                    f"Getter is expected to be a method, got {type(fget).__name__} instead."
                )

            lSignature = signature(fset)
            lParamList = list(lSignature.parameters.values())
            if len(lParamList) != 2:
                raise TypeError(
                    f"Setter is expected to accept exactly two arguments, got {len(lParamList)} instead."
                )

            lParam = lParamList[1]
            if not Is(lParam.annotation, lReturnType):
                raise Exception(
                    f'Setter requires {lReturnType}, got "{lParam.annotation}" instead.'
                )

        if fdel is not None:
            if not callable(fdel):
                raise TypeError(
                    f"Deleter is expected to be a method, got {type(fdel).__name__} instead."
                )

        super().__init__(fget, fset, fdel, doc)
        self._attributeName: str = None
        self._key: str = None
        self._type = lReturnType
        self._owner: type = None

    def __set_name__(self, owner: type, name: str):
        self._attributeName = name
        self._owner = owner
        self._key = f"_{name.strip().lower()}"

    def _get(self, instance: Any):
        return self.fget(instance)  # type: ignore

    def __get__(self, instance: Any, owner: Optional[type] = None) -> _ValueType:
        if owner is None:
            return self  # type: ignore

        if self.fget is None:
            raise AttributeError(f"unreadable attribute '{self._attributeName}'")

        if owner is not None and not isinstance(instance, owner):
            return default(self._type)

        return self._get(instance)

    def _set(self, instance, value: _ValueType):
        self.fset(instance, value)

    def __set__(self, instance: Any, value: _ValueType) -> None:
        def _validateSet(inst: "Property", _value: _ValueType) -> None:
            if self.fset is None:
                raise AttributeError(f"Property {self._attributeName} is readonly")

            if self._attributeName == "":
                raise AttributeError("Property not intialized yet")

            if not Is(_value, self._type):
                lTypeName = getattr(self._type, "__name__", str(self._type))
                lClass = getattr(inst, "__class__", {})
                lOwnerName = lClass.__name__ or "object"
                raise TypeError(
                    f"{lOwnerName}.{self._attributeName} Expected type '{lTypeName}', but got '{type(_value).__name__}'."
                )

        def _doSet(inst: object, _value: _ValueType):
            lOldValue: _ValueType = self.__get__(inst, type(inst))

            self._set(inst, _value)

            if hasattr(inst, "OnPropertyChanged"):
                lValueChanged: bool = False
                try:
                    lNewValue: _ValueType = self.__get__(inst, type(inst))
                    lValueChanged = lOldValue != lNewValue

                    if lValueChanged:
                        lOnChangedProperty = getattr(inst, "OnPropertyChanged", None)
                        lOnChangedProperty.emit(
                            inst, self._attributeName, lOldValue, lNewValue
                        )

                except AttributeError:
                    pass

                except Exception as e:
                    raise RuntimeError(
                        f"Error setting property {self._attributeName} value"
                    ) from e

        _validateSet(instance, value)
        return _doSet(instance, value)

    def __delete__(self, obj: Any) -> None:
        if self.fdel is None:
            raise AttributeError(f"can't delete attribute '{self._attributeName}'")

        self.fdel(obj)

    def Getter(self, fget: Callable[[Any], _ValueType]) -> "Property":
        return Property(fget=fget, fset=self.fset, fdel=self.fdel, doc=self.__doc__)

    def Setter(self, fset: Callable[[Any, _ValueType], None]) -> "Property":
        return Property(fget=self.fget, fset=fset, fdel=self.fdel, doc=self.__doc__)

    def Deleter(self, fdel: Callable[[Any], None]) -> "Property":
        return Property(fget=self.fget, fset=self.fset, fdel=fdel, doc=self.__doc__)
