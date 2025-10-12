from json import load

from jAGFx.configuration import ApplicationConfiguration, LoggerConfig, iConfiguration
from jAGFx.dependencyInjection import Provider

LOGGER_SECTION = "LOGGER"
DB_CONFIG_PATH: str = "config/db/appconfig.json"


class DashboardConfiguration(ApplicationConfiguration):
    def __init__(self, title: str = "", company: str = "", appid: str = "", icon: str = "") -> None:
        super().__init__(title, company, appid, icon)

        self._tagspath: str = ".\\assets\\tags"
        self.Properties.append("TagsPath")

    @property
    def TagsPath(self) -> str:
        self._tagspath = self._tagspath.replace("/", "\\")
        if self._tagspath.endswith("\\"):
            self._tagspath = self._tagspath[:-1]
        return self._tagspath

    @TagsPath.setter
    def TagsPath(self, value: str) -> None:
        self._tagspath = value

def LoadCFG(path: str = DB_CONFIG_PATH) -> DashboardConfiguration:
    cfg: DashboardConfiguration = DashboardConfiguration()

    with open(path) as file:
        cfgdict: dict = load(fp=file)

    cfg.decode(cfgdict)

    return cfg


Provider.RegisterFactory(iConfiguration, LoadCFG, DashboardConfiguration, True)
