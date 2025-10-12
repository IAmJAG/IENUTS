from inspect import isfunction
from typing import TypeVar

from ..singleton import SingletonF
from ..types import Is

T = TypeVar("T")

__all__ = ["default", "registerTypeDefault", "unregisterTypeDefault"]


@SingletonF
class TypeDefaults(dict[type[T], T | None]):
    pass


def default(typ: type[T]) -> T | None:
    try:
        if typ in TypeDefaults():
            lObj = TypeDefaults()[typ]

            # if the default is a class type, call it to get the default value
            if isinstance(lObj, type):
                return lObj()
            return lObj

        return None

    except TypeError:
        return None

    except NotImplementedError:
        return None

    except Exception as e:
        raise e


def registerTypeDefault(typ: type[T], default: T) -> None:
    if not Is(default, typ):
        if isfunction(default):
            return registerTypeDefault(typ, default())
        else:
            raise TypeError(
                f"Default value must be an instance or subclass of {typ.__qualname__}."
            )

    TypeDefaults()[typ] = default


def unregisterTypeDefault(typ: type[T]) -> None:
    del TypeDefaults()[typ]


# DEFAULTS
registerTypeDefault(str, "")
registerTypeDefault(int, 0)
registerTypeDefault(float, 0.0)
registerTypeDefault(bool, False)
registerTypeDefault(list, [])
registerTypeDefault(dict, {})
registerTypeDefault(set, set())
