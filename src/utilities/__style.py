# src/eNuts/utilities/__style.py
import os
import re

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from jAGFx.logger import debug, error
from jAGFx.utilities.io import getFontPath, getStylePath

QSSVARREGEX = r"--(\w+):\s*([^;]+);"  # variable regex (--<*>)
QSSLHREGEX = r"--\w+:\s*[^;]+;"  # placehorder regex (@<*>)


def LoadQSS(qss: str, theme: str = "basic"):
    def _PreProcQSS(_qss: str):
        lVariables: dict = {}
        for lMatch in re.finditer(QSSVARREGEX, _qss):
            lVariables[lMatch.group(1)] = lMatch.group(2).strip()

        _qss = re.sub(QSSLHREGEX, "", _qss)

        for lName, lValue in lVariables.items():
            _qss = _qss.replace(f"@{lName}", lValue)

        return _qss.strip()

    with open(f"{getStylePath(f'{qss}.qss')}") as lFile:
        lQSS = lFile.read()

    try:
        lProcessedQSS = _PreProcQSS(lQSS)
        QApplication.instance().setStyleSheet(lProcessedQSS)
        debug(f"applied styles from {qss}")

    except Exception as lE:
        error("Error loading QSS", lE)


def LoadFonts() -> list[str]:
    lLoadedFonts: list[str] = list[str]()
    lFontDir: str = getFontPath()
    for lFileName in os.listdir(lFontDir):
        if lFileName.endswith((".ttf", ".otf")):
            lFontPath = os.path.join(lFontDir, lFileName)
            lFontId = QFontDatabase.addApplicationFont(lFontPath)
            if lFontId != -1:
                lFamilies = QFontDatabase.applicationFontFamilies(lFontId)
                if lFamilies:
                    for lFamily in lFamilies:
                        if lFamily not in lLoadedFonts:
                            debug(f"Font loaded: {lFamily}")

                    lLoadedFonts.extend(lFamilies)

    return sorted(list(set(lLoadedFonts)))
