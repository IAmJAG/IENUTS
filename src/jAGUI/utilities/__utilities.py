# ==================================================================================
import os

# ==================================================================================
from json import dump, load

# ==================================================================================
from PySide6.QtGui import QIcon, QImage, QPixmap

# ==================================================================================
from jAGFx.configuration import ApplicationConfiguration, iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.overload import OverloadDispatcher
from jAGFx.utilities.io import getConfigPath

__all__ = ["GetImage", "LoadCFG", "SaveCFG", "newIcon"]


def LoadCFG(path: str = getConfigPath("appconfig.json")) -> ApplicationConfiguration:
    with open(path) as file:
        jsonData = load(fp=file)
        cfg: ApplicationConfiguration = ApplicationConfiguration()
        cfg.decode(jsonData)
    return cfg


def SaveCFG(path: str = getConfigPath("appconfig.json")):
    cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)  # type: ignore
    with open(path, "w") as file:
        cfg = dump(cfg.encode(), fp=file)


def _getImagePath(imgfile: str) -> str:
    cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)  # type: ignore
    for lExt in cfg.ImagesExtensions:
        lImagePath = f"{imgfile}{lExt}".strip()
        if os.path.exists(lImagePath):
            return lImagePath

    for lPath in cfg.ImagesPaths:
        for lExt in cfg.ImagesExtensions:
            lImagePath = f"{lPath}/{imgfile}{lExt}".strip()
            if os.path.exists(lImagePath):
                return lImagePath

    return ""


@OverloadDispatcher
def newIcon(path: str = "application-default-icon", disable: bool = False) -> QIcon:
    def _getIconFromPath(iconName: str) -> QIcon:
        if os.path.exists(iconName):
            return QIcon(iconName)
        elif os.path.exists(f"{iconName}.png"):
            return QIcon(f"{iconName}.png")
        elif os.path.exists(f".\\assets\\icons\\{iconName}"):
            return QIcon(f".\\assets\\icons\\{iconName}")
        elif os.path.exists(f".\\assets\\icons\\{iconName}.png"):
            return QIcon(f".\\assets\\icons\\{iconName}.png")

        return QIcon.fromTheme(path)

    icon = _getIconFromPath(path)

    if icon.isNull():
        return QIcon.fromTheme("application-default-icon")

    if disable:
        pixmap = icon.pixmap(icon.actualSize(icon.availableSizes()[0]))
        grayscale = pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
        icon = QIcon(QPixmap.fromImage(grayscale))

    return icon


@newIcon.overload
def newIcon(icon: QIcon, disable: bool) -> QIcon:
    if disable:
        pixmap = icon.pixmap(icon.actualSize(icon.availableSizes()[0]))
        grayscale = pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
        return QIcon(QPixmap.fromImage(grayscale))
    return icon


@OverloadDispatcher
def GetImage(path: str) -> QPixmap:
    cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)  # type: ignore

    lImagePath = _getImagePath(path)
    if lImagePath.strip() == "":
        raise Exception(f"Image {path} not found")

    if path == cfg.Icon:
        return None

    lImage = QPixmap(lImagePath)
    if lImage.isNull():
        raise Exception(f"Failed to load icon: {path}")

    return lImage


@GetImage.overload
def GetImage(img: QPixmap) -> QPixmap:
    return img
