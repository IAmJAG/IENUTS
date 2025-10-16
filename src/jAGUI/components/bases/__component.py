# ==================================================================================
import inspect
import weakref

# ==================================================================================
from threading import current_thread, main_thread

# ==================================================================================
from PySide6.QtCore import QCoreApplication, QObject, QSettings, Qt, QThread, Signal
from PySide6.QtWidgets import QBoxLayout, QMainWindow, QScrollArea, QTabWidget, QWidget

# ==================================================================================
from jAGFx.configuration import ApplicationConfiguration, iConfiguration
from jAGFx.dependencyInjection.Providers import Provider
from jAGFx.property import Property
from jAGFx.utilities import getRandomNames

# ==================================================================================
from ...contracts import iComponent
from ..utilities import convertSquareSides


class Component(iComponent):
    Invoke: Signal = Signal(str, object, object)
    def __init__(self, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(self, QWidget):
            raise ValueError(
                f"Subclass Error: expected subclass of QWidget but got {type(self).__name__}"
            )

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        if name is None or name.strip() == "":
            name = getRandomNames(4, 8)

        if parent is not None and not isinstance(parent, QWidget | QMainWindow):
            raise Exception(
                "Invalid parent type",
                TypeError(
                    f"Parent is expected to be a QWidget or subclass of QWidget, got {type(parent).__name__}"
                ),
            )

        if parent is not None:
            self.setParent(parent)

        self.setObjectName(name)

        def _invoke(methodName: str, args, kwargs):
            method = getattr(self, methodName)
            if callable(method):
                return method(*args, **kwargs)

            raise TypeError(f"{methodName} is not callable.")

        self.Invoke.connect(_invoke)

        weakref.ref(self, self._cleanUp)

    def _cleanUp(self):
        if isinstance(self, QWidget):
            self.setParent(None)

    def Load(self): ...

    def setupUI(self, layout: QBoxLayout | None = None):
        if layout is None:
            layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
            layout.setObjectName(f"{self.FQN}-{self.Name.upper()}-LAYOUT")
            layout.setContentsMargins(*convertSquareSides(0))
            layout.setSpacing(0)

        if isinstance(self, QWidget):
            self.setLayout(layout)

        else:
            raise ValueError(
                f"Subclass Error: expected subclass of QWidget but got {type(self).__name__}"
            )

    @property
    def InvokeRequired(self) -> bool:
        return QThread.currentThread() != QCoreApplication.instance().thread()

    def invoke(self, *args, **kwargs):
        frame = inspect.currentframe()
        caller_frame = frame.f_back if frame else None
        method_name = caller_frame.f_code.co_name if caller_frame else None
        if not method_name or not hasattr(self, method_name):
            raise AttributeError("No current method set or method does not exist.")

        self.Invoke.emit(method_name, args, kwargs)

    @property
    def ContentSpacing(self):
        return self.Layout.spacing()

    @ContentSpacing.setter
    def ContentSpacing(self, value: int):
        self.Layout.setSpacing(value)

    @property
    def ContentMargins(self):
        return self.Layout.contentsMargins()

    @ContentMargins.setter
    def ContentMargins(self, value: int | tuple[int] | list[int]):
        self.Layout.setContentsMargins(*convertSquareSides(value))

    @property
    def Layout(self) -> QBoxLayout:
        if isinstance(self, QWidget):
            return self.layout()

        raise ValueError(
            f"Subclass Error: expected subclass of QWidget but got {type(self).__name__}"
        )

    @Layout.setter
    def Layout(self, value: QBoxLayout) -> None:
        if isinstance(self, QWidget):
            self.setLayout(value)
            return

        raise ValueError(
            f"Subclass Error: expected subclass of QObject but got {type(self).__name__}"
        )

    @Property
    def Parent(self) -> QObject:
        if isinstance(self, QObject):
            return self.parent()

        raise ValueError(
            f"Subclass Error: expected subclass of QObject but got {type(self).__name__}"
        )

    @Parent.setter
    def Parent(self, value: QObject):
        if isinstance(self, QObject):
            self.setParent(value)
            self.update()

    @property
    def Name(self) -> str:
        if isinstance(self, QObject):
            return self.objectName()

        raise ValueError(
            f"Subclass Error: expected subclass of QObject but got {type(self).__name__}"
        )

    @Name.setter
    def Name(self, value: str):
        if isinstance(self, QWidget):
            self.setObjectName(value)
            self.update()
        else:
            raise ValueError(
                f"Subclass Error: expected subclass of QObject but got {type(self).__name__}"
            )

    @property
    def Settings(self) -> QSettings:
        if not hasattr(self, "_settings"):
            cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)

            self._settings = QSettings()
            if hasattr(cfg, "Company") and hasattr(cfg, "AppId"):
                self._settings = QSettings(cfg.Company, cfg.AppId)

            else:
                raise Exception("Invalid settings, cfg not consistent")

        return self._settings

    @property
    def IsVisible(self) -> bool:
        if isinstance(self, QWidget):
            return self.isVisible()

        raise ValueError(
            f"Subclass Error: expected subclass of QWidget but got {type(self).__name__}"
        )

    @IsVisible.setter
    def IsVisible(self, value: bool):
        if isinstance(self, QWidget):
            self.setVisible(value)

        else:
            raise ValueError(
                f"Subclass Error: expected subclass of QWidget but got {type(self).__name__}"
            )

    @property
    def MainWindow(self) -> QMainWindow:
        def _getMainWindow():
            _mainwindow: QMainWindow = self
            while _mainwindow is not None and not isinstance(_mainwindow, QMainWindow):
                if hasattr(_mainwindow, "Parent"):
                    _mainwindow = _mainwindow.Parent
                    continue

                if hasattr(_mainwindow, "parent"):
                    _mainwindow = _mainwindow.parent()
                    continue

                raise Exception("Cound not find Mainwindow")

            if _mainwindow is None:
                raise Exception("Cound not find Mainwindow")

            return _mainwindow

        lMainWindow: QMainWindow
        if not hasattr(self, "_mainwindow"):
            self._mainwindow: QMainWindow = None

        if self._mainwindow is None:
            lMainWindow = _getMainWindow()
            if lMainWindow is None:
                raise Exception("Cound not find Mainwindow")

            self._mainwindow = lMainWindow

        return self._mainwindow

    @property
    def IsObscured(self) -> bool:
        if not self.isVisible():
            return True

        # Check ancestors for visibility and TabWidget
        parent: QWidget = self.parentWidget()
        while parent:
            if not parent.isVisible():
                return True

            if (
                isinstance(parent, QTabWidget)
                and parent.currentWidget() != self.parentWidget()
            ):
                return True

            parent = parent.parentWidget()

        # Check for QScrollArea viewport
        parent = self.parentWidget()
        while parent:
            if isinstance(parent, QScrollArea):
                lViewPort = parent.viewport()
                lWidGlobalRect = self.mapToGlobal(self.rect())
                lViewPortGlobalRect = lViewPort.mapToGlobal(lViewPort.rect())
                if not lViewPortGlobalRect.intersects(lWidGlobalRect):
                    return True
                break  # Only need to check the immediate scroll area parent

            parent = parent.parentWidget()

        # Check top-level window visibility and state
        lTopLevel = self.window()
        if not lTopLevel.isVisible() or (
            lTopLevel.windowState() & Qt.WindowState.WindowMinimized
        ):
            return True

        # Heuristic check for overlapping sibling widgets (very basic)
        parent = self.parentWidget()
        if parent:
            lWidRect = self.geometry()
            for sibling in parent.children():
                if (
                    sibling != self
                    and isinstance(sibling, QWidget)
                    and sibling.isVisible()
                ):
                    sibling_rect = sibling.geometry()
                    if (
                        sibling_rect.intersects(lWidRect)
                        and sibling.zValue() >= self.zValue()
                    ):
                        # Basic Z-order comparison - might not be fully accurate
                        return True
        return False
