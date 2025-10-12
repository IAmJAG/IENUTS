from threading import current_thread, main_thread

from jAGFx.logger import info
from jAGFx.singleton import SingletonF
from PySide6.QtCore import Q_ARG, QMetaObject, Qt, QTimer, Slot
from PySide6.QtWidgets import QBoxLayout, QLabel, QSizePolicy, QWidget

from ..bases import ComponentBase
from ..resizeGrip import ResizeGrip
from ..utilities import processMarker

STATUS_BAR_HEIGHT = 25

def Status(msg: str, timeout: int = 0):
    lStatusBar = StatusBar()

    if main_thread().ident == current_thread().ident:
        lStatusBar.showMessage(msg, timeout)

    else:
        QMetaObject.invokeMethod(
            lStatusBar,
            "showMessage",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(str, msg),
            Q_ARG(int, timeout)
        )

@SingletonF
@processMarker(True, True)
class StatusBar(ComponentBase):
    def __init__(self, name: str = '', parent: QWidget = None, *args, **kwargs):  #type: ignore
        super().__init__(name, parent)

    def Load(self):
        super().Load()
        self._messageTimer.timeout.connect(self.clearMessage)

    def setupUI(self, layout = None):
        super().setupUI(layout)
        self.Layout.setDirection(QBoxLayout.Direction.LeftToRight)
        self.setFixedHeight(STATUS_BAR_HEIGHT)

        lStatus = QLabel(text="")
        lStatus.setObjectName("StatusLabel")
        lStatus.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._status = lStatus

        lResizeGrip = ResizeGrip()

        lResizeLayout: QBoxLayout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        lResizeLayout.addStretch()
        lResizeLayout.addWidget(lResizeGrip)
        lResizeGrip.setParent(self)

        self.Layout.addWidget(self._status)
        self.Layout.addItem(lResizeLayout)
        self.Layout.setStretchFactor(self._status, 1)

        self._messageTimer = QTimer(self)
        self._messageTimer.setSingleShot(True)

    @Slot(str, int)
    def showMessage(self, text: str, timeout: int = 0):
        info(text)
        self._status.setText(text)
        if timeout == 0:
            self._messageTimer.stop()
        else:
            self._messageTimer.start(timeout)

    def clearMessage(self):
        self._status.setText("")
