from logging import Filter, getLevelNamesMapping
from typing import Any, Optional

from ..singleton import SingletonM
from .__filter import Filter as xFilter


class Singleton(SingletonM):
    def __call__(self, *args, **kwargs) -> Any:
        instance: LogFilter = super().__call__(*args, **kwargs)
        try:
            if len(args) > 0:
                if kwargs.get("module", None) is not None:
                    lModules: dict[str, str] = kwargs.get("module", None)  # type: ignore

                if kwargs.get("level", None) is not None:
                    lLevel: str = kwargs.get("level", "DEBUG")

                if isinstance(args[0], list):
                    lLevel: str = args[1]
                    lModules: dict[str, str] = args[0]  # type: ignore

                for lModule in lModules:
                    instance.AddFilter(lModule, lLevel)

            return instance
        except Exception as ex:
            raise ex


class LogFilter(Filter, metaclass=Singleton):
    def __init__(self, modules: Optional[list[str]] = None, level="DEBUG"):
        super().__init__()
        self._filters: dict[str, xFilter] = dict[str, xFilter]()

        if modules is None:
            modules = []

        for lMod in modules:
            self._filters[lMod] = xFilter(lMod, level)  # type: ignore

    @property
    def Filters(self):
        return self._filters

    def AddFilter(self, module, level):
        if module not in self._filters:
            self._filters[module] = xFilter(module, level)

    def RemoveFilter(self, module: str):
        self._filters.pop(module, None)

    def filter(self, record):
        if getattr(record, "caller", None) is None:
            record.caller = "NOTMINE.ALL"

        if len(self._filters) > 0 and record is not None:
            # Check if the record's module is in the filters
            lCaller: str = str(getattr(record, "caller", None))

            if lCaller is not None and lCaller != "":
                lNamespaces: list[str] = lCaller.split(".")
                for i in range(len(lNamespaces)):
                    lNamespace: str = ".".join(lNamespaces[: len(lNamespaces) - i])
                    if lNamespace in self._filters:
                        lFilter = self._filters[lNamespace]
                        return record.levelno >= getLevelNamesMapping()[lFilter.Level]

        return record is not None


def AddFilter(namespace: str, level: str = "DEBUG"):
    LogFilter([namespace], level)


def RemoveFilter(namespace: str, level: str = "DEBUG"):
    LogFilter().RemoveFilter(namespace)
