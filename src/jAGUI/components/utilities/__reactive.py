from collections import deque
from functools import wraps
from multiprocessing import Lock

from jAGFx.property import Property
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QScrollArea, QTabWidget, QWidget

RC_LOCK = Lock()
REACTIVECOMPONETS: deque = deque()


def _updateFocused(focused: QWidget):
    with RC_LOCK:
        if focused in REACTIVECOMPONETS:
            REACTIVECOMPONETS.remove(focused)

        REACTIVECOMPONETS.append(focused)


def reactive(cls: type[QWidget]):
    if not issubclass(cls, QWidget):
        raise Exception("Invalid argument type", TypeError(f"Reactive expect a QWidget or subclass of QWidget, got {cls.__name__}"))

    lOrigInit = cls.__init__
    @wraps(lOrigInit)
    def _newInit(self: QWidget, *args, **kwargs):
        lOrigInit(self, *args, **kwargs)
        _updateFocused(self)

        self.installEventFilter(self)

    @Property # type: ignore
    def IsReactive(self) -> bool:
        return self._isreactive

    @Property # type: ignore
    def IsObscured(self: QWidget) -> bool:  # noqa: C901
        if not self.isVisible(): return True

        # Check ancestors for visibility and TabWidget
        parent = self.parentWidget()
        while parent:
            if not parent.isVisible(): return True
            if isinstance(parent, QTabWidget) and parent.currentWidget() != self.parentWidget(): return True
            parent = parent.parentWidget()

        # Check for QScrollArea viewport
        parent = self.parentWidget()
        while parent:
            if isinstance(parent, QScrollArea):
                viewport = parent.viewport()
                widget_rect_global = self.mapToGlobal(self.rect()) # type: ignore
                viewport_rect_global = viewport.mapToGlobal(viewport.rect()) # type: ignore
                if not viewport_rect_global.intersects(widget_rect_global):
                    return True
                break  # Only need to check the immediate scroll area parent
            parent = parent.parentWidget()

        # Check top-level window visibility and state
        top_level = self.window()
        if not top_level.isVisible() or (top_level.windowState() & Qt.WindowState.WindowMinimized):
            return True

        # Heuristic check for overlapping sibling widgets (very basic)
        parent = self.parentWidget()
        if parent:
            widget_rect = self.geometry()
            for sibling in parent.children():
                if sibling != self and isinstance(sibling, QWidget) and sibling.isVisible():
                    sibling_rect = sibling.geometry()
                    if sibling_rect.intersects(widget_rect) and sibling.zValue() >= self.zValue():  # type: ignore
                        # Basic Z-order comparison - might not be fully accurate
                        return True

        return False

    cls.IsReactive = IsReactive
    cls.IsObscured = IsObscured

    lOrigEventFilter = cls.eventFilter
    @wraps(lOrigEventFilter)
    def eventFilter(self, watched, event):
        lRet = lOrigEventFilter(watched, event) if lOrigEventFilter is not None else super(cls, self).eventFilter(watched, event)  # type: ignore

        global REACTIVEONFOCUSED
        if event.type() == QEvent.FocusIn and self.isVisible() and not self.isObscured(): # type: ignore
            _updateFocused(self)

        # elif event.type() == QEvent.Show:
        #     _updateListOrder()
        # elif event.type() == QEvent.Hide:
        #     _updateListOrder()

        return lRet

    cls.__init__ = _newInit
    cls.eventFilter = eventFilter

    return cls
