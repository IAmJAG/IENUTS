from jAGFx.utilities.io import getICONPath
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyle

from ...exception import IconNotFoundException


def getIcon(iconPath: str):
    lIcon: QIcon = QIcon(getICONPath(iconPath))
    if lIcon.isNull():
        lAppStyle: QStyle = QApplication.instance().style()
        lIcon = lAppStyle.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
        if lIcon.isNull():
            raise IconNotFoundException()
    return lIcon
