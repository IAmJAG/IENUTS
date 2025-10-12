from datetime import datetime
from enum import Enum
from inspect import isfunction
from typing import get_type_hints

from ..contracts.serializer import iSerialisable


def _decodeEnum(lType, obj):
    try:
        lMember = obj.get("__member__", None)
        lNewObj = lType[lMember]  # type: ignore
        return lNewObj

    except Exception as ex:
        raise Exception(f"Error retrieving enum type {lType.__class__.__name__}") from ex

def _decodeSerializeable(lType: type, obj):
    try:
        lNewObj = lType()
        lNewObj.decode(obj)
        return lNewObj

    except Exception as ex:
        raise Exception(f"Error occur initializing {lType.__name__}") from ex

def _decodeFunction(lType, obj):
    lReturnType: type = get_type_hints(lType)
    if lReturnType is not None:
        if issubclass(lReturnType, iSerialisable):
            lNewObj: iSerialisable = lType()
            lNewObj.decode(obj)
            return lNewObj
    return None

def _decodeCustomType(obj):
    lClass: str = obj.get("__type__", None)
    if lClass is not None:
        try:
            lModuleName, lClassName = lClass.rsplit('.', 1)
            lModule = __import__(lModuleName, fromlist=[lClassName])
            lType = getattr(lModule, lClassName)

            if issubclass(lType, Enum):
                return _decodeEnum(lType, obj)

            elif issubclass(lType, iSerialisable):
                return _decodeSerializeable(lType, obj)

            else:
                if isfunction(lType):
                    lNewObj = _decodeFunction(lType, obj)
                    if lNewObj is not None:
                        return lNewObj

                obj.pop("__type__", None)
                lNewObj = lType(**obj)
                return lNewObj

        except ModuleNotFoundError as ex:
            raise Exception(f"Module {lClass} not found!") from ex

        except Exception as e:
            raise Exception(f"Error trying to deserialize {type(obj).__name__}") from e

    return None

def jsonDecode(obj: dict):
    try:
        if isinstance(obj, list):
            return [jsonDecode(lVal) for lVal in obj]

        elif isinstance(obj, tuple):
            return (jsonDecode(lVal) for lVal in obj)

        elif isinstance(obj, dict):
            lNewObj = _decodeCustomType(obj)
            if lNewObj is not None:
                return lNewObj

            elif "__datetime__" in obj:
                lNewObj = datetime.fromisoformat(obj["__datetime__"])
                return lNewObj
            else:
                return {lKey: jsonDecode(lValue) for lKey, lValue in obj.items()}

    except Exception as ex:
        raise ex

    return obj
