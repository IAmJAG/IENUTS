# ==================================================================================
from typing import Any
from uuid import uuid4

# ==================================================================================
from PySide6.QtCore import QRect, QRectF

# ==================================================================================
from jAGFx.overload import OverloadDispatcher
from jAGFx.serializer import Serialisable


class BoundingBox(QRectF, Serialisable):
    @OverloadDispatcher
    def __init__(self, klass: str, rect: QRectF, id: str) -> None:
        super().__init__(rect)
        self._id: str = id or str(uuid4())
        self._class = klass
        self._origin = False
        self.Properties.extend(["X", "Y", "W", "H", "Class", "Id", "Origin"])

    @__init__.overload
    def __init__(self, klass: str, rect: QRectF) -> None:
        self.__init__(klass, rect, str(uuid4()))

    @__init__.overload
    def __init__(self, dct: dict) -> None:
        lModule: list[str] = self.__module__.split(".")
        if lModule[len(lModule) - 1].startswith("__"):
            lModule: str = ".".join(lModule[:-1])

        else:
            lModule: str = ".".join(lModule)


        if dct["__type__"] == f"{lModule}.{type(self).__name__}":
            try:
                self.__init__(dct["Class"], QRect(dct["X"], dct["Y"], dct["W"], dct["H"]), dct["Id"])
                self._origin = dct["Origin"]
                return

            except KeyError:
                raise Exception("Invalid data provided!")

        raise Exception(f"Invalid entity class, expecting a {lModule}.{type(self).__name__}")


    @property
    def Class(self) -> str:
        return self._class

    @Class.setter
    def Class(self, value: str):
        self._class = value

    @property
    def Origin(self) -> bool:
        return self._origin

    @Origin.setter
    def Origin(self, value: bool):
        self._origin = value

    @property
    def Left(self) -> float:
        return self.x()

    @property
    def Right(self) -> float:
        return self.y()

    @property
    def X(self) -> float:
        return self.x()

    @property
    def Y(self) -> float:
        return self.y()

    @property
    def W(self) -> float:
        return self.width()

    @property
    def H(self) -> float:
        return self.height()

    @property
    def center(self) -> tuple[float, float]:
        return (self.X + (self.W / 2), self.Y + (self.H / 2))

    @property
    def area(self) -> int:
        return self.width() * self.height()

    def toTuple(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

    @property
    def Id(self) -> str:
        return self._id

    def _encodeProperty(self, prop: str):
        if prop == "Tags":
            return None

        if prop == "X":
            return self.x(), False

        if prop == "Y":
            return self.y(), False

        if prop == "H":
            return self.height(), False

        if prop == "W":
            return self.width(), False

        if prop == "Origin":
            return self._origin, False

        return super()._encodeProperty(prop)

    def decode(self, dct: Any):
        lModule: list[str] = self.__module__.split(".")
        if lModule[len(lModule) - 1].startswith("__"):
            lModule: str = ".".join(lModule[:-1])

        else:
            lModule: str = ".".join(lModule)

        if dct["__type__"] == f"{lModule}.{type(self).__name__}":
            self._class = dct["Class"]
            self._id = (dct["Id"])
            self._origin = dct.get("Origin", False)
            self.setX(dct["X"])
            self.setY(dct["Y"])
            self.setWidth(dct["W"])
            self.setHeight(dct["H"])
