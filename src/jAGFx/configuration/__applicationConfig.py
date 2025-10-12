from json import load
from typing import TypeVar

from ..dependencyInjection import Provider
from .__configuration import Configuration, iConfiguration
from .__logger import LoggerConfig

__all__ = ["ApplicationConfiguration"]

LOGGER_SECTION = "LOGGER"


class ApplicationConfiguration(Configuration):
    def __init__(
        self,
        title: str = "",
        company: str = "",
        appid: str = "",
        icon: str = "",
    ) -> None:
        super().__init__()

        self._title: str = title
        self._company: str = company
        self._appid: str = appid
        self._icon: str = icon
        self._style: str = "style"

        self._imagespaths: list[str] = list[str]()
        self._imagesextensions: list[str] = list[str]()

        self.Properties.extend(
            [
                "Title",
                "Company",
                "AppId",
                "Icon",
                "StyleDefaults",
                "Style",
                "ImagesPaths",
                "ImagesExtensions",
            ]
        )

    @property
    def ImagesPaths(self) -> list[str]:
        return self._imagespaths

    @property
    def ImagesExtensions(self) -> list[str]:
        return self._imagesextensions

    @property
    def Sections(self) -> dict[str, iConfiguration]:
        return super().Sections

    @property
    def Style(self) -> str:
        return self._style

    @property
    def Title(self) -> str:
        return self._title

    @property
    def Company(self) -> str:
        return self._company

    @property
    def AppId(self) -> str:
        return self._appid

    @property
    def Icon(self) -> str:
        return self._icon

    @property
    def Logger(self) -> LoggerConfig:
        if self.Sections.get(LOGGER_SECTION, None) is None:
            self.Sections[LOGGER_SECTION] = LoggerConfig()

        lLoggerSection: LoggerConfig = self.Sections[LOGGER_SECTION]

        return lLoggerSection


T = TypeVar("T", bound=Configuration)


def LoadCFG(path: str = "config/appconfig.json") -> ApplicationConfiguration:
    cfg: ApplicationConfiguration = ApplicationConfiguration()

    with open(path) as file:
        cfgStr: str = load(fp=file)

    cfg.decode(cfgStr)

    return cfg


Provider.RegisterFactory(iConfiguration, LoadCFG, ApplicationConfiguration, True)
