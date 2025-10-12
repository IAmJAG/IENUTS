from typing import Callable

from jAGFx.utilities.io import getICONPath
from jAGFx.utilities.names import getRandomNames
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QPushButton, QSizePolicy, QWidget

from ...types import eCommandPosition
from ..bases import ContainerBase
from ..utilities import processMarker


@processMarker(True, True)
class CommandBar(ContainerBase):
    def __init__(self, name: str = "", parent=None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)
        self._buttons: dict[str, QPushButton] = dict[str, QPushButton]()

    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.Layout.setDirection(QBoxLayout.Direction.LeftToRight)

        self._leftContainer: ContainerBase = ContainerBase()
        self._leftContainer.Layout.setDirection(QBoxLayout.Direction.LeftToRight)

        self._rightContainer: ContainerBase = ContainerBase()
        self._rightContainer.Layout.setDirection(QBoxLayout.Direction.RightToLeft)

        self.AddComponent(self._leftContainer)
        self.AddStretch()
        self.AddComponent(self._rightContainer)

    @property
    def Buttons(self) -> dict[str, QPushButton]:
        return self._buttons

    def AddSeparator(self, width: int = 10, pos: eCommandPosition = eCommandPosition.LEFT):
        lSeparator: QWidget = QWidget()
        lSeparator.setObjectName("CMDBARSEPARATOR")
        lSeparator.setFixedWidth(width)
        lSeparator.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        lContainer: ContainerBase = self._leftContainer if pos == eCommandPosition.LEFT else self._rightContainer
        lContainer.AddComponent(lSeparator)

    def AddCommand(self, text: str, cb: Callable[[QPushButton], None], name: str = "", pos: eCommandPosition = eCommandPosition.LEFT, icon: QIcon = None):
        name = getRandomNames() if name is None or name.strip() == "" else name
        lBtn: QPushButton = QPushButton(text, objectName=name)

        if icon is not None:
            if isinstance(icon, str):
                icon = QIcon(getICONPath(icon))
            lBtn.setIcon(icon)

            lBtn.setIconSize(QSize(self.height(), self.height()))

        lBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        def _clicked():
            lBtn.setEnabled(False)
            try:
                cb(lBtn)

            except Exception as ex:
                raise ex

            finally:
                lBtn.setEnabled(True)

        lBtn.clicked.connect(_clicked)
        self._buttons.update({name: lBtn})

        lContainer: ContainerBase = self._leftContainer if pos == eCommandPosition.LEFT else self._rightContainer
        lContainer.AddComponent(lBtn)
