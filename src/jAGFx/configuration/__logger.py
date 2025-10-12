
from jAGFx.serializer import Serialisable


class ILoggerFilter:
    @property  # type: ignore
    def DefaultLogLevel(self) -> str: ...

    @property  # type: ignore
    def Module(self) -> str: ...


class ILoggerFiltersConfig:
    @property  # type: ignore
    def DefaultLogLevel(self) -> str: ...

    @property  # type: ignore
    def Filters(self) -> list[ILoggerFilter]: ...


class LoggerFilter(Serialisable, ILoggerFilter):
    def __init__(self, level: str = "DEBUG") -> None:
        super().__init__()
        self._defaultloglevel: str = level
        self._modules: list[dict[str, str]] = list[dict[str, str]]()
        self.Properties.extend(["DefaultLogLevel", "Module"])

    @property  # type: ignore
    def DefaultLogLevel(self) -> str:
        return self._defaultloglevel

    @property  # type: ignore
    def Module(self) -> list[dict[str, str]]:
        return self._modules


class LoggerConfig(Serialisable, ILoggerFiltersConfig):
    def __init__(self):
        super().__init__()
        self._defaultloglevel = "DEBUG"
        self._filters: dict[str, ILoggerFilter] = dict[str, ILoggerFilter]()
        self.Properties.extend(["DefaultLogLevel", "Filters"])

    @property  # type: ignore
    def DefaultLogLevel(self) -> str:
        return self._defaultloglevel

    @property  # type: ignore
    def Filters(self) -> dict[str, ILoggerFilter]:
        return self._filters
