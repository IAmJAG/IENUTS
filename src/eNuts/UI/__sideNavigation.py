from typing import Any

from jAGFx.logger import warning
from jAGUI.components import Button
from jAGUI.components.navigation import SideNavigationBar, _navigationBar
from jAGUI.components.utilities import processMarker
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QWidget

from .mwHelper import MenuInfo

REGDEVKEY: str = "REGISTEREDDEVICES"
ICONSIZE: int = 36


@processMarker(True, True)
class Navigation(SideNavigationBar):
    OnButtonClicked: Signal = Signal(Button)
    OnMenuCreated: Signal = Signal(Button, Any)

    def __init__(self, text: str, ico: str | QIcon = "logo.png", parent: QWidget = None, *lArgs, **lKwargs):
        super().__init__(text, ico, parent, *lArgs, **lKwargs)
        self._devices: dict[str, Button] = dict[str, Button]()
        self._buttons: dict[str, MenuInfo] = dict[str, MenuInfo]()
        self._expand()

    def Load(self):
        super().Load()

    def setupUI(self, layout: QBoxLayout | None = None):
        super().setupUI(layout)

    def AddMenu(self, title: str, icon: QIcon, id: str, isParent: bool = False, parentId: str = ""):
        lLayout: QBoxLayout
        lLevel: int = 0
        if parentId.strip() == "":
            lLayout = self.Layout

        else:
            if parentId in self._buttons:
                lParent = self._buttons[parentId]
                lLayout = lParent.ChildBar.Layout
                lLevel = 1 + lParent.Level

            else:
                warning("Parent menu not found, adding to the root")
                lLayout = self.Layout
                lLevel = 0

        lIconSize: int = ICONSIZE - (lLevel * 2)
        lBtn: Button = Button(title, icon)
        setattr(lBtn, "buttonId", id)
        lBtn.setMaximumHeight(40 - (5 * lLevel))
        lBtn.setObjectName(f"MENUBUTTON{lLevel:02d}")
        lBtn.setIconSize(QSize(lIconSize, lIconSize - 5))
        lBtn.PadLeft = 10 + (lLevel * 10)

        lCBar: _navigationBar = None
        if isParent:
            # if tagged as parent create a childbar

            lCBar: _navigationBar = _navigationBar(_navigationBar.eDrawerOrientation.VERTICAL)
            lBtn.setCheckable(False)

            # enclose both button and child bar in a layout
            lGLayout: QBoxLayout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
            lGLayout.setContentsMargins(0, 0, 0, 0)
            lGLayout.setSpacing(0)

            lGLayout.addWidget(lBtn)
            lGLayout.addWidget(lCBar)
            lLayout.addLayout(lGLayout)
        else:
            lLayout.addWidget(lBtn)

        def _select(btn: Button):
            if self._buttons[btn.buttonId].ChildBar is None:
                for info in self._buttons.values():
                    if info.Button.isCheckable():
                        info.Button.setChecked(info.Button == btn and info.ChildBar is None)

        lBtn.OnClicked.connect(_select)

        self._buttons[id] = MenuInfo(lBtn, lCBar, lLevel, parentId)
        return lBtn
