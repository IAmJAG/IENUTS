from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout

from jAGFx.logger import debug


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self._itemList: list = []
        self._expandingOrientation = Qt.Vertical

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._itemList.append(item)
        self.update()

    def count(self):
        return len(self._itemList)

    def itemAt(self, index):
        if 0 <= index < len(self._itemList):
            return self._itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._itemList):
            return self._itemList.pop(index)
        return None

    def expandingDirections(self) -> Qt.Orientation:
        return self._expandingOrientation

    def setExpandingDirections(self, orientation: Qt.Orientation):
        self._expandingOrientation = orientation
        self.update()

    def hasHeightForWidth(self):
        return self._expandingOrientation == Qt.Vertical

    def heightForWidth(self, width):
        return self._doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        return size + QSize(margins.left() + margins.right(), margins.top() + margins.bottom())

    def _doLayout(self, rect, isTest: bool):
        margins = self.contentsMargins()

        if self._expandingOrientation == Qt.Vertical:
            # Horizontal flow: left to right, wrap down
            x = rect.x() + margins.left()
            y = rect.y() + margins.top()
            line_height = 0

            for i, item in enumerate(self._itemList):
                item_width = item.sizeHint().width()
                if x + item_width > rect.right() - margins.right() and line_height > 0:
                    x = rect.x() + margins.left()
                    y += line_height + self.spacing()
                    line_height = 0

                if not isTest:
                    item_rect = QRect(QPoint(x, y), item.sizeHint())
                    item.setGeometry(item_rect)

                x += item_width + self.spacing()
                line_height = max(line_height, item.sizeHint().height())

            height = y + line_height - rect.y() + margins.top() + margins.bottom()
            return height

        else:
            # Vertical flow: top to bottom, wrap right
            x = rect.x() + margins.left()
            y = rect.y() + margins.top()
            column_width = 0

            for i, item in enumerate(self._itemList):
                item_height = item.sizeHint().height()
                if y + item_height > rect.bottom() - margins.bottom() and column_width > 0:
                    x += column_width + self.spacing()
                    y = rect.y() + margins.top()
                    column_width = 0

                if not isTest:
                    item_rect = QRect(QPoint(x, y), item.sizeHint())
                    item.setGeometry(item_rect)

                y += item_height + self.spacing()
                column_width = max(column_width, item.sizeHint().width())

            width = x + column_width - rect.x() + margins.left() + margins.right()
            return width  # For heightForWidth, return the width needed
