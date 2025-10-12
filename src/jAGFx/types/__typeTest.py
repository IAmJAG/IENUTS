import collections.abc
from inspect import Parameter, isclass
from types import UnionType
from typing import Any, Union, get_origin

EMPTYSTRING = ""

__all__ = ["Is", "isNone", "isPrimitive", "isTypeAny", "isUnionType"]


def isNumeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def isScalar(obj):
    return isPrimitive(obj)


def isPrimitive(obj):
    return type(obj) in [int, float, bool, str] or obj is None


def isTypeAny(paramType):
    return paramType == Parameter.empty or paramType == Any or paramType == any


def isNone(paramType):
    return paramType is None or paramType == EMPTYSTRING


def isUnionType(paramType):
    return (hasattr(paramType, "__origin__") and paramType.__origin__ is Union) or type(
        paramType
    ) is UnionType


def isGeneric(tp: type) -> bool:
    return get_origin(tp) is not None


def _isStandardType(provided: Any, expectedType: type) -> bool:
    if provided != expectedType:
        if isclass(provided):
            return issubclass(provided, expectedType)
        else:
            return isinstance(provided, expectedType)
    else:
        return True


def _isGenericType(provided: Any, expectedType: type, expected_origin) -> bool:
    if isclass(provided):
        provided_origin = get_origin(provided)
        compare_provided = provided_origin if provided_origin is not None else provided

    elif (
        getattr(provided, "__orig_bases__", None) is not None
        and get_origin(provided) is not None
    ):
        provided_origin = get_origin(provided)
        return Is(provided_origin, expected_origin)
    else:
        compare_provided = type(provided)

    try:
        if isclass(compare_provided):
            if expected_origin is collections.abc.Sequence:
                return issubclass(compare_provided, collections.abc.Sequence)
            if expected_origin is collections.abc.Mapping:
                return issubclass(compare_provided, collections.abc.Mapping)
            return issubclass(compare_provided, expected_origin)

        return False

    except TypeError:
        return False


def Is(provided: Any, expectedType: type) -> bool:
    try:
        return _isStandardType(provided, expectedType)

    except TypeError:
        try:
            if isinstance(provided, expectedType):
                return True

        except TypeError:
            pass

        expected_origin = get_origin(expectedType)

        if expected_origin is Union:
            return isUnionType(provided)

        if expected_origin is not None:
            return _isGenericType(provided, expectedType, expected_origin)

        return False
    except Exception:
        return False
