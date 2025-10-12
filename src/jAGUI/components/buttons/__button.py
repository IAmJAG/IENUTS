from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtGui import QFontMetrics, QIcon, QPainter, QPaintEvent, QPalette
from PySide6.QtWidgets import QAbstractButton, QLayout, QStyle, QStyleOptionButton, QWidget

from ...contracts import iPushButton
from ...types import eIconAlignment
from ..bases import Component
from ..utilities import processMarker

DEFAULT_ICON_SIZE: QSize = QSize(36, 36)


@processMarker(True, True)
class Button(Component, QAbstractButton):
    OnClicked: Signal = Signal(iPushButton, bool)
    OnPressed: Signal = Signal(iPushButton)
    OnReleased: Signal = Signal(iPushButton)
    OnToggled: Signal = Signal(iPushButton)

    def __init__(self, text: str = "Pushbutton", icon: QIcon = None, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)
        self._textAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        self._iconAlignment: eIconAlignment = eIconAlignment.LEFT

        self._padleft: int = 5
        self._padright: int = 5

        lIcon: QIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation) if icon is None else icon
        self.setText(text)
        self.setIcon(lIcon)

        super().clicked.connect(lambda toggled: self.OnClicked.emit(self, toggled))
        super().pressed.connect(lambda: self.OnPressed.emit(self))
        super().released.connect(lambda: self.OnReleased.emit(self))
        super().toggled.connect(lambda: self.OnToggled.emit(self))

    def setupUI(self, layout: QLayout = None):
        super().setupUI(layout)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setMouseTracking(True)
        self.setIconSize(DEFAULT_ICON_SIZE)

    def paintEvent(self, event: QPaintEvent):
        lOption = QStyleOptionButton()
        lOption.initFrom(self)

        if self.isChecked():
            lOption.state |= QStyle.StateFlag.State_On
        if self.isDown():
            lOption.state |= QStyle.StateFlag.State_Sunken
        if self.underMouse():
            lOption.state |= QStyle.StateFlag.State_MouseOver

        with QPainter(self) as lPainter:
            self.style().drawControl(QStyle.ControlElement.CE_PushButton, lOption, lPainter, self)
            self.drawContent(lPainter)

    def drawContent(self, painter: QPainter):
        lIcon = self.icon()
        lText = self.text()

        lRect = self.rect()
        lContentRect = QRect(lRect)

        lIconSize = self.iconSize()
        lIconPixmap = lIcon.pixmap(lIconSize)

        lIconRect = QRect()
        lTextRect = QRect()

        if not lIconPixmap.isNull() and lText:
            lPad = self._padleft
            lHSpace = 10
            if self._iconAlignment == eIconAlignment.RIGHT:
                lPad = self._padright

            lIconRect.setSize(lIconSize)
            lTextRect.setSize(QSize(lRect.width() - lIconSize.width() - lPad - lHSpace, lRect.height()))

            # Calculate icon position
            if self._iconAlignment == eIconAlignment.LEFT:
                lIconRect.setLeft(lPad)
                lTextRect.setLeft(lPad + lIconSize.width() + lHSpace)
            else:
                lIconRect.setRight(lRect.width() - lPad)
                lTextRect.setRight(lRect.width() - lPad - lIconSize.width() - lHSpace)

            lIconRect.moveCenter(QPoint(lIconRect.center().x(), lRect.center().y()))
            lTextRect.moveCenter(QPoint(lTextRect.center().x(), lRect.center().y()))

        elif not lIconPixmap.isNull():
            # Only icon is present
            lIconRect.setSize(lIconSize)
            lIconRect.moveCenter(lRect.center())
            self.setToolTip(lText)

        elif lText:
            # Only text is present
            lTextRect.setRect(lRect.left() + self._padleft, lRect.top(), lRect.width() - self._padleft - self._padright, lRect.height())
            self.setToolTip("")

        # Draw the elements
        if not lIconPixmap.isNull():
            painter.drawPixmap(lIconRect, lIconPixmap)

        if lText:
            self.style().drawItemText(painter, lTextRect, self.TextAlignment, self.palette(), self.isEnabled(), lText, QPalette.ColorRole.ButtonText)

    def sizeHint(self) -> QSize:
        lFM = QFontMetrics(self.font())
        lTextWidh = lFM.horizontalAdvance(self.text())
        lEstimatedWidth = self.iconSize().width() + 2 * 10 + lTextWidh
        return QSize(max(self.minimumSizeHint().width(), lEstimatedWidth), self.height())

    def minimumSizeHint(self) -> QSize:
        return QSize(self.iconSize().width() + 2 * 5, self.height())

    @property
    def Text(self) -> str:
        return self.text()

    @Text.setter
    def Text(self, value: str):
        self.setText(value)
        self.update()

    @property
    def IconAlignment(self) -> eIconAlignment:
        return self._iconAlignment

    @IconAlignment.setter
    def IconAlignment(self, value: eIconAlignment):
        self._iconalignment = value
        self.update()

    @property
    def TextAlignment(self):
        return self._textAlignment

    @TextAlignment.setter
    def TextAlignment(self, val: Qt.AlignmentFlag):
        self._textAlignment = val
        self.update()

    @property
    def PadLeft(self) -> int:
        return self._padleft

    @PadLeft.setter
    def PadLeft(self, value: int):
        self._padleft = value
        self.update()

    @property
    def PadRight(self) -> int:
        return self._padright

    @PadRight.setter
    def PadRight(self, value: int):
        self._padright = value
        self.update()

    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update()
