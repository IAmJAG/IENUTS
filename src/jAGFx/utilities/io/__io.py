import os

ASSETSDIR: str = "assets"
CONFIGDIR: str = "config"
FONTDIR: str = "fonts"
STYLEDIR: str = "styles"
ICONDIR: str = "icons"


def getAssetPath(assetDirectory: str):
    lDir: str = os.path.join(os.getcwd(), ASSETSDIR)
    return os.path.join(lDir, assetDirectory)


def getStylePath(styleFileName: str = ""):
    lPath: str = STYLEDIR if styleFileName.strip() == "" else os.path.join(STYLEDIR, styleFileName)
    return os.path.join(ASSETSDIR, lPath)


def getFontPath(fontFilename: str = ""):
    lPath: str = FONTDIR if fontFilename.strip() == "" else os.path.join(FONTDIR, fontFilename)
    return os.path.join(os.getcwd(), ASSETSDIR, lPath)


def getICONPath(iconFilename: str = ""):
    lPath: str = ICONDIR if iconFilename.strip() == "" else os.path.join(ICONDIR, iconFilename)
    return os.path.join(os.getcwd(), ASSETSDIR, lPath)


def getConfigPath(relativePath: str):
    lDir: str = os.path.join(os.getcwd(), CONFIGDIR)
    return os.path.join(lDir, relativePath)
