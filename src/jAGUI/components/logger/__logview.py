from datetime import datetime
from logging import CRITICAL, DEBUG, ERROR, FATAL, INFO, WARNING
from multiprocessing import Lock

from jAGFx.overload import OverloadDispatcher
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QBoxLayout, QSizePolicy, QTextEdit, QWidget

from ..bases import Component

LOG_COLOR_MAP: dict[int, QColor] = {
    DEBUG: QColor("blue"),
    INFO: QColor("green"),
    WARNING: QColor("yellow"),
    ERROR: QColor("amber"),
    CRITICAL: QColor("red"),
    FATAL: QColor("magenta")
}


class logViewer(Component, QTextEdit):
    def __init__(self, name: str = '', parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)

        self._lastdate: str = None
        self._statlock = Lock()

    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

    @OverloadDispatcher
    def Status(self, text: str):
        self.Status(text, INFO)

    @Status.overload
    def Status(self, text: str, logLevel: int, timestamp: datetime):
        if isinstance(timestamp, QDateTime):
            self.Status(text, logLevel, timestamp)
        else:
            self.Status(text, logLevel, QDateTime(timestamp))

    @Status.overload
    def Status(self, text: str, logLevel: int, timestamp: QDateTime):
        lBracketFormat: QTextCharFormat = QTextCharFormat()
        lBracketFormat.setFont(self.font())
        lBracketFormat.setForeground(QColor("cyan"))
        lBracketFormat.setFontWeight(QFont.Weight.Bold)

        lCursor: QTextCursor = self.textCursor()

        lCurrDate: str = QDateTime.currentDateTime().toString("MMddyyyy")
        if self._lastdate != lCurrDate:
            self._lastdate: str = lCurrDate

            lDateFormat: QTextCharFormat = QTextCharFormat()
            lDateFormat.setFont(self.font())
            lDateFormat.setForeground(QColor("red"))
            lDateFormat.setFontWeight(QFont.Weight.Bold)

            lCursor.movePosition(QTextCursor.MoveOperation.End)
            lCursor.beginEditBlock()
            lCursor.insertText("[", lBracketFormat)
            lCursor.insertText(f"{self._lastdate}", lDateFormat)
            lCursor.insertText("]", lBracketFormat)
            self.setTextCursor(lCursor)

        lTimeformat: QTextCharFormat = QTextCharFormat()
        lTimeformat.setForeground(QColor("lightgray"))
        lTimeformat.setFontWeight(QFont.Weight.Normal)

        # Create a new character format
        lTextformat = QTextCharFormat()
        lTextformat.setForeground(LOG_COLOR_MAP[logLevel])
        lTextformat.setFontWeight(QFont.Weight.DemiBold)

        if isinstance(timestamp, QDateTime):
            lTime = f"{timestamp.toString('hh:mm:ss')}"
        else:
            lTime = f"{QDateTime(timestamp).toString('hh:mm:ss')}"

        lCursor = self.textCursor()
        lCursor.movePosition(QTextCursor.MoveOperation.End)

        if lCursor.position() != 0:
            lCursor.insertText("\n")

        lCursor.beginEditBlock()
        lCursor.insertText("  [", lBracketFormat)
        lCursor.insertText(lTime, lTimeformat)
        lCursor.insertText("]", lBracketFormat)
        lCursor.insertText(f"  {text}", lTextformat)
        lCursor.endEditBlock()

        try:
            self.setTextCursor(lCursor)
            self.update()

        except Exception as ex:
            raise ex


    @Status.overload
    def Status(self, text: str, logLevel: int):
        self.Status(text, logLevel, QDateTime.currentDateTime())
