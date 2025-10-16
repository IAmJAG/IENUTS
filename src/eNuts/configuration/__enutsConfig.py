# src/eNuts/configuration/__enutsConfig.py
from json import load

from jAGFx.configuration import ApplicationConfiguration, LoggerConfig, iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.singleton import SingletonC

SCRCPY_SECTION = "SCRCPY"
LOGGER_SECTION = "LOGGER"
LOGGER_FILTERS = "filters"
LOGGER_FILTERS_LEVEL = "defaultFilterLevel"


@SingletonC
class ENUTSConfig(ApplicationConfiguration):
    def __init__(self, title: str = "", company: str = "", appid: str = "", icon: str = "") -> None:
        super().__init__(title, company, appid, icon)

    @property
    def Logger(self) -> LoggerConfig:
        if self.Sections.get(LOGGER_SECTION, None) is None:
            self.Sections[LOGGER_SECTION] = LoggerConfig()  # type: ignore

        lLoggerSection: LoggerConfig = self.Sections[LOGGER_SECTION]  # type: ignore

        return lLoggerSection

    def _encodeProperty(self, prop: str):
        return super()._encodeProperty(prop)

    def _decodeProperty(self, dct: dict, prop: str):
        return super()._decodeProperty(dct, prop)


CFG: ENUTSConfig = None


def LoadCFG(path: str) -> ENUTSConfig:
    global CFG
    if CFG is None:
        with open(path) as file:
            cfgO = load(fp=file)

        CFG = ENUTSConfig()
        CFG.decode(cfgO)

    return CFG


# Provider.RegisterSingleton(iConfiguration, ApplicationConfiguration, dependent=ENUTSConfig)
Provider.RegisterFactory(iConfiguration, LoadCFG, path="config/appconfig.json")
