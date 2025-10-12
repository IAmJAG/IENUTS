import datetime
from enum import Enum
from typing import Any
from weakref import ref as wref

from ..contracts.serializer import iSerialisable
from .__utilities import jsonDecode


class Serialisable(iSerialisable):
    def __init__(self) -> None:
        super().__init__()
        self._properties: list[str] = []

        wref(self, self.cleanUp)

    @property
    def Properties(self) -> list[str]:
        return self._properties

    def _encodeProperty(self, prop: str):
        def _exEncode(obj: Serialisable | Any):
            if isinstance(obj, dict):
                return {k: _exEncode(v) for k, v in obj.items()}

            if isinstance(obj, list):
                return [_exEncode(v) for v in obj]

            if isinstance(obj, tuple):
                return tuple(_exEncode(v) for v in obj)

            if isinstance(obj, Serialisable):
                return obj.encode()

            if isinstance(obj, Enum):
                lEnum = {
                    "__member__": obj.name,
                    "__type__": f"{obj.__module__}.{type(obj).__name__}",
                }
                return lEnum

            if isinstance(obj, datetime.datetime):
                return {"__datetime__": obj.isoformat()}

            return obj

        lProp = _exEncode(getattr(self, f"_{prop.lower()}", None))
        return lProp, False

    def _decodeProperty(self, dct: Any, lProp: str):
        return dct.get(lProp, None)

    def encode(self) -> dict[str, object]:
        lDict: dict = {}
        for lProp in self.Properties:
            try:
                lValue, lSkip = self._encodeProperty(lProp)
                if lSkip:
                    continue
                lDict[lProp] = lValue

            except KeyError as ke:
                raise Exception(
                    f"Error encoding {type(self).__name__}",
                    KeyError(f"Could not find {lProp} key '_{lProp.lower()}'"),
                ) from ke

            except Exception as e:
                raise Exception(
                    f"Unhandled exception from encoding {type(self).__name__}"
                ) from e

        lModule: list[str] = self.__module__.split(".")

        if lModule[len(lModule) - 1].startswith("__"):
            lModule: str = ".".join(lModule[:-1])

        else:
            lModule: str = ".".join(lModule)

        lDict["__type__"] = f"{lModule}.{type(self).__name__}"

        return lDict

    def decode(self, dct: Any):
        errors = []
        for lProp in self.Properties:
            try:
                if lProp in self.Properties:
                    lVal = self._decodeProperty(dct, lProp)
                    if lVal is not None:
                        lVal = jsonDecode(lVal)
                        setattr(self, f"_{lProp.strip().lower()}", lVal)

            except KeyError:  # noqa: PERF203
                errors.append(
                    Exception(
                        f"Error decoding {type(self).__name__}",
                        KeyError(f"Could not find {lProp} key '_{lProp.lower()}'"),
                    )
                )

            except Exception:
                errors.append(
                    Exception(
                        f"Unhandled exception from decoding {type(self).__name__}"
                    )
                )

        if errors:
            raise Exception(f"Decoding encountered {len(errors)} error(s): {errors}")
