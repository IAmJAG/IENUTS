# src/eNuts/utilities/__style.py
import os
import re
from time import sleep

from jAGFx.logger import debug, error
from jAGFx.utilities.io import getFontPath, getStylePath
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

QSSVARREGEX = r"--(\w+):\s*([^;]+);"  # variable regex (--<*>)
QSSLHREGEX = r"--\w+:\s*[^;]+;"  # placehorder regex (@<*>)


def LoadQSS(qss: str, theme: str = "basic"):
    def _preProcQSS(_qss: str):
        lVariables: dict = {}
        for match in re.finditer(QSSVARREGEX, _qss):
            lVariables[match.group(1)] = match.group(2).strip()

        _qss = re.sub(QSSLHREGEX, "", _qss)

        for lName, lValue in lVariables.items():
            _qss = _qss.replace(f"@{lName}", lValue)

        return _qss.strip()

    with open(f"{getStylePath(f'{qss}.qss')}") as file:
        lQSS = file.read()

    try:
        lProccessedQSS = _preProcQSS(lQSS)
        QApplication.instance().setStyleSheet(lProccessedQSS)
        debug(f"applied styles from {qss}")

    except Exception as e:
        error("Error loading QSS", e)


def LoadFonts() -> list[str]:
    lLoadedFonts: list[str] = list[str]()
    lFontDir: str = getFontPath()
    for lFilename in os.listdir(lFontDir):
        if lFilename.endswith((".ttf", ".otf")):
            lFontPath = os.path.join(lFontDir, lFilename)
            lFontId = QFontDatabase.addApplicationFont(lFontPath)
            if lFontId != -1:
                lFamilies = QFontDatabase.applicationFontFamilies(lFontId)
                if lFamilies:
                    for lFamily in lFamilies:
                        if lFamily not in lLoadedFonts:
                            debug(f"Font loaded: {lFamily}")

                    lLoadedFonts.extend(lFamilies)

    return sorted(list(set(lLoadedFonts)))
