import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from adbutils import AdbDevice
from jAGFx.logger import debug, error
from jAGUI.components import Button
from jAGUI.components.forms import FormBasic
from jAGUI.components.statusBar import StatusBar
from jAGUI.components.titleBar import TitleBar
from jAGUI.components.utilities import getIcon, processMarker
from PySide6.QtGui import QIcon, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QApplication, QBoxLayout, QFileDialog, QPushButton, QSizePolicy, QWidget

from ..contracts import iDeviceMonitor
from ..scrcpy import mapCode
from ..scrcpy.const import *
from ..services import SCRCPYStreamService
from ..utilities.runnables import DeviceMonitor
from .__sideNavigation import Navigation
from .mwHelper import *
from .pages import *
from .streamerClients import StreamerClient

REGDEVKEY: str = "REGISTEREDDEVICES"
ICONSIZE: int = 36
VIDEODIR: str = "VIDEODIR"
WORKERS: int = 20


@processMarker(True, True)
class MainWindow(FormBasic):
    EXECUTOR: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=WORKERS)

    def __init__(self, enableTools: bool = False, *args):
        super().__init__(True)
        self._registeredDevices: dict[str, dict] = self.Settings.value(REGDEVKEY, {})
        # self.Settings.remove(VIDEODIR)

        self._streamers: dict[str, StreamerClient] = dict[str, StreamerClient]()
        self._pageStack: dict[str, QWidget] = dict[str, QWidget]()
        self._currentPage: QWidget = None
        self._enableTools: bool = enableTools

    def Load(self):
        super().Load()
        lMonitor: iDeviceMonitor = DeviceMonitor()
        lMonitor.start()
        lMonitor.OnDeviceAdded.connect(self._onDeviceAdded)
        lMonitor.OnDeviceRemoved.connect(self._onDeviceRemoved)

    def setupUI(self) -> None:
        super().setupUI()
        lTitleBar: TitleBar = TitleBar(self)
        lStatusBar = StatusBar()

        lBaseLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.LeftToRight)
        lContentLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.TopToBottom)

        lNavBar: Navigation = Navigation(self.Title, self.windowIcon())
        lNavBar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        lNavBar.setObjectName("NAVIGATIONBAR")

        lBaseLayout.addWidget(lNavBar)
        lBaseLayout.addLayout(lContentLayout, 1)
        lBaseLayout.setStretchFactor(lContentLayout, 0)

        self.AddComponent(lTitleBar)
        self.Layout.addLayout(lBaseLayout)
        self.AddComponent(lStatusBar)

        self._navbar: Navigation = lNavBar
        self._contentLayout = lContentLayout
        self._createMenu()

    # region [DEVICE EVENTS]
    def _onDeviceAdded(self, device: AdbDevice):
        # lProduct: str = device.shell(["getprop", "ro.product.model"])

        lStreamer: SCRCPYStreamService = SCRCPYStreamService(device.serial, 1250, 5000)  ## passing adb serial
        lClient: StreamerClient = StreamerClient(lStreamer, lStreamer.DeviceName)

        lFunc = self._getRecorder if self._enableTools else None
        lDevicePage = StreamerPage(f"{lStreamer.ADBSerial.upper()}", lClient, lStreamer.ADBSerial.upper(), lFunc)
        self._devicePage(lStreamer.ADBSerial, getIcon("smartphone.png"), lStreamer.ADBSerial, lDevicePage, "DEVICES")
        self._streamers[lStreamer.ADBSerial] = lClient

        lClient.mousePressEvent = self._mouseEvent(lClient.Streamer, ACTION_DOWN)
        lClient.mouseMoveEvent = self._mouseEvent(lClient.Streamer, ACTION_MOVE)
        lClient.mouseReleaseEvent = self._mouseEvent(lClient.Streamer, ACTION_UP)

        def _resize(w, h):
            if lClient.isVisible():
                self.resize(1, 1)

        lClient.OnResolutionChanged.connect(_resize)

    def _onDeviceRemoved(self, device: AdbDevice):
        try:
            lBtn: Button = self._devices.pop(device.serial)
            lBtn.setParent(None)

        except KeyError:
            print("xxx")
            pass

        except Exception:
            error("Error occur trying to remove device.")

    # endregion

    # region [PROPERTIES]
    @property
    def NavigationBar(self) -> Navigation:
        return self._navbar

    @property
    def PageStack(self) -> dict[str, QWidget]:
        return self._pageStack

    # endregion

    def _switchPage(self, page):
        if self._currentPage is not None:
            self._contentLayout.removeWidget(self._currentPage)
            self._currentPage.setParent(None)

        self._contentLayout.addWidget(page)
        self._currentPage = page

    def _devicePage(self, title: str, icon: QIcon, key: str, page: QWidget, parentMenuKey: str = ""):
        lNavBar: Navigation = self.NavigationBar
        lBtn: Button = lNavBar.AddMenu(title, icon, key, parentId=parentMenuKey)
        lBtn.setCheckable(True)

        def _gOnClicked(_page):
            def _onClicked(btn):
                self._switchPage(self.PageStack[btn.buttonId])
                QApplication.instance().processEvents()
                for strmr in self._streamers.values():
                    strmr.setVisible(strmr.Streamer.ADBSerial.upper() == btn.buttonId.upper())
                    if strmr.isVisible():
                        if not strmr.Streamer.isAlive:
                            strmr.Start()

            return _onClicked

        lBtn.OnClicked.connect(_gOnClicked(page))
        self.PageStack[lBtn.buttonId] = page

    def _navigationPage(self, title: str, icon: QIcon, key: str, page: QWidget, parentMenuKey: str = ""):
        lBtn: Button = self.NavigationBar.AddMenu(title, icon, key, parentId=parentMenuKey)
        lBtn.setCheckable(True)
        lBtn.OnClicked.connect(lambda btn: self._switchPage(self.PageStack[btn.buttonId]))
        self.PageStack[lBtn.buttonId] = page

    def _createMenu(self):
        self._navigationPage("Dashboard", getIcon("UIUX\\dashboard.png"), "DASHBOARD", Dashboard())
        self.NavigationBar.AddMenu("Devices", getIcon("local-area.png"), "DEVICES", True)
        self.NavigationBar.Layout.addStretch()
        self._switchPage(next(iter(self.PageStack.values())))

    # region [KBM events]
    def _mouseEvent(self, strmr: SCRCPYStreamService, action=ACTION_DOWN):
        def handler(evt: QMouseEvent):
            lFocusWidget = QApplication.focusWidget()
            if lFocusWidget is not None:
                lFocusWidget.clearFocus()

            strmr.Control.touch(
                evt.position().x() / strmr.SizeRatio,
                evt.position().y() / strmr.SizeRatio,
                action,
            )

        return handler

    def _keyEvent(self, strmr: SCRCPYStreamService, action=ACTION_DOWN):
        def handler(evt: QKeyEvent):
            code = mapCode(evt.key())
            if code != -1:
                strmr.Control.keycode(code, action)

        return handler

    # endregion

    def closeEvent(self, event):
        for strmr in self._streamers.values():
            strmr.Stop()
        super().closeEvent(event)

    def _getRecorder(self, _strmr: StreamerClient):
        def _record(btn: QPushButton):
            strmr = _strmr.Streamer

            def _executeRecord():
                btn.setDisabled(True)
                if btn.text() == "Record Video":
                    try:
                        lTimeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename: str = f"{lTimeStamp}.mp4"
                        os.makedirs(lVideoPath, exist_ok=True)
                        lLocalPath = f"{lVideoPath}\\{filename}"
                        strmr.Device.start_recording(lLocalPath)
                        btn.setText("Stop Recording")

                    except Exception as ex:
                        error("Error occur on trying to record video", ex)
                        btn.setText("Record Video")

                    finally:
                        btn.setDisabled(False)

                else:
                    try:
                        strmr.Device.stop_recording()
                        btn.setText("Record Video")

                    except Exception as ex:
                        error("Error occur on trying to retrieve recorded video", ex)
                        btn.setText("Record Video")

                    finally:
                        btn.setText("Record Video")
                        btn.setDisabled(False)

            btn.setDisabled(True)
            try:
                lVideoPath: str = self.Settings.value(VIDEODIR, None)
                if lVideoPath is None:
                    lDDialog = QFileDialog(self)
                    lDDialog.setFileMode(QFileDialog.Directory)
                    lDDialog.setOption(QFileDialog.ShowDirsOnly, True)
                    if lDDialog.exec():
                        lSelectedDir = lDDialog.selectedFiles()
                        if lSelectedDir:
                            lVideoPath = lSelectedDir[0]
                            self.Settings.setValue(VIDEODIR, lVideoPath)

                if lVideoPath is None:
                    debug("No path selected!")
                    return

                self.EXECUTOR.submit(_executeRecord)

            except Exception as ex:
                btn.setDisabled(False)
                error("An error occur while recording video", ex)

        return _record
