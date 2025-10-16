from typing import Any

from jAGFx.overload import OverloadDispatcher
from jAGFx.serializer import Serialisable


class Tag(Serialisable):
    @OverloadDispatcher
    def __init__(self) -> None:
        super().__init__()
        self.Properties.extend(["Code", "Text", "Description"])

    @__init__.overload
    def __init__(self, dct: dict) -> None:
        lModule: list[str] = self.__module__.split(".")
        if lModule[len(lModule) - 1].startswith("__"):
            lModule: str = ".".join(lModule[:-1])
        else:
            lModule: str = ".".join(lModule)

        if dct["__type__"].strip() == f"{lModule}.{type(self).__name__}".strip():
            try:
                self.__init__(dct["Code"], dct["Text"], dct.get("Description", ""))
                return

            except KeyError as ke:
                raise KeyError("Invalid data provided!") from ke

            except Exception as ex:
                raise ex

        else:
            raise Exception(f"Invalid entity class, expecting a {lModule}.{type(self).__name__} got {dct['__type__']}")

    @__init__.overload
    def __init__(self, code: int, text: str) -> None:
        self.__init__(code, text, "")

    @__init__.overload
    def __init__(self, code: int, text: str, description: str) -> None:
        self.__init__()
        if not isinstance(code, int) or code <= 0 or (code & (code - 1)) != 0:
            raise ValueError("Code must be a positive integer that is a power of 2")

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")

        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        self._code = code
        self._text = text
        self._description = description

    @property
    def Code(self) -> int:
        return self._code

    @property
    def Text(self) -> str:
        return self._text

    @property
    def Description(self) -> str:
        return self._description

    @Description.setter
    def Description(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value

    def _encodeProperty(self, prop: str):
        if prop == "Code":
            return self._code, False

        if prop == "Text":
            return self._text, False

        if prop == "Description":
            return self._description, False

        return super()._encodeProperty(prop)

    def __repr__(self):
        return f"Tag(code={self._code}, text='{self._text}', description='{self._description}')"
