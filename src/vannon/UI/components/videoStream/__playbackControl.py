# ==================================================================================
import os

# ==================================================================================
from numpy import ndarray

# ==================================================================================
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QFileDialog, QLabel, QSlider, QWidget

# ==================================================================================
from jAGFx.exceptions import jAGException
from jAGFx.logger import warning
from jAGFx.utilities.io import getICONPath

# ==================================================================================
from jAGUI.components import ComponentBase
from jAGUI.components.utilities import processMarker

# ==================================================================================
from utilities.mwHelper import CreateButton, InitializeLayout

# ==================================================================================
from ....contracts import iVideoThread
from ....exceptions import InvalidFileException
from ....videoThread import MediaInfo, eMediaState, ePlaybackState

VIDEODIR: str = "VIDEODIR"

@processMarker(True, True)
class PlaybackControls(ComponentBase):
    def __init__(self, vt: iVideoThread, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)

        self._vt: iVideoThread = vt

    def Load(self):
        super().Load()
        del self._vt

    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.ContentMargins = [5, 0, 5, 5]

        lVT: iVideoThread = self._vt

        lFrameSlider = QSlider(Qt.Orientation.Horizontal)
        lFrameSlider.setRange(0, 100)

        lFrameLabel = QLabel("00:00:00")

        lSliderLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.LeftToRight)
        lSliderLayout.setSpacing(7)
        lSliderLayout.addWidget(lFrameSlider)
        lSliderLayout.addWidget(lFrameLabel)

        lPrevButton = CreateButton("", icon=QIcon(getICONPath("video\\backward.png")))
        lPlayButton = CreateButton("", icon=QIcon(getICONPath("video\\play.png")))
        lNextButton = CreateButton("", icon=QIcon(getICONPath("video\\forward.png")))

        lLoadButton = CreateButton("", icon=QIcon(getICONPath("video\\videoclip.png")))

        lButtonsLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.LeftToRight)
        lButtonsLayout.setSpacing(2)
        lButtonsLayout.addWidget(lPrevButton)
        lButtonsLayout.addWidget(lPlayButton)
        lButtonsLayout.addWidget(lNextButton)
        lButtonsLayout.addStretch()
        lButtonsLayout.addWidget(lLoadButton)

        self.Layout.addLayout(lSliderLayout)
        self.Layout.addLayout(lButtonsLayout)

        lNextButton.setEnabled(False)
        lPrevButton.setEnabled(False)
        lPlayButton.setEnabled(False)

        lSliderPressed: bool = False

        def _onFrame(frame: ndarray, frameIndex: int):
            lSeconds = frameIndex / lVT.FPS
            lMs = int((lSeconds - int(lSeconds)) * 100)
            lTime = f"{frameIndex:04d} - {int(lSeconds // 60):02d}:{int(lSeconds % 60):02d}:{lMs:02d}"

            lFrameLabel.setText(lTime)
            if frameIndex >= 0 and not lVT.IsSeeking:
                lFrameSlider.blockSignals(True)
                lFrameSlider.setValue(frameIndex)
                lFrameSlider.blockSignals(False)

        def _onMediaLoaded(mi: MediaInfo):
            lFrameSlider.setRange(0, mi.FrameCount - 1)

        def _onMediaStateChange(state: eMediaState):
            lNextButton.setEnabled(state == eMediaState.LOADED)
            lPrevButton.setEnabled(state == eMediaState.LOADED)
            lPlayButton.setEnabled(state == eMediaState.LOADED)

            if state == eMediaState.LOADED:
                lFrameSlider.setValue(0)

            else:
                lFrameSlider.setRange(0, 0)
                lFrameLabel.setText("0000 - 00:00:00")

        def _onPlaybackStateChanged(state: ePlaybackState):
            lICO: QIcon
            if state == ePlaybackState.PLAYING:
                lICO = QIcon(getICONPath("video\\pause.png"))
            else:
                lICO = QIcon(getICONPath("video\\play.png"))

            lPlayButton.setIcon(lICO)
            lLoadButton.setEnabled(state != ePlaybackState.PLAYING)

        lVT.OnMediaLoaded.connect(_onMediaLoaded)
        lVT.OnFrame.connect(_onFrame)
        lVT.OnMediaStateChanged.connect(_onMediaStateChange)
        lVT.OnPlaybackStateChanged.connect(_onPlaybackStateChanged)

        def _loadVideoFile():
            lDefaultDIR = self.Settings.value(VIDEODIR, "")
            lFilepath, _ = QFileDialog.getOpenFileName(self, "Open Video", lDefaultDIR, "Video Files (*.mp4 *.avi *.mov)")
            if lFilepath:
                self.Settings.setValue(VIDEODIR, os.path.dirname(lFilepath))
                lVT.stopPlayback()
                try:
                    lVT.setVideoFile(lFilepath)

                except InvalidFileException as ex:
                    # progress.setVisible(False)
                    warning(f"Error opening {lFilepath}", ex)

                except Exception:
                    raise jAGException(f"{self.FQN}: Error occur while openning video file {lFilepath}")

        def _playPause():
            if lVT.PlaybackState & ePlaybackState.PLAYING == ePlaybackState.PLAYING:
                lVT.pause()

            else:
                lVT.play()

        nlPreviousState: ePlaybackState = ePlaybackState.STOPPED

        # region [SLIDER SLOTS]
        def _onSliderPressed():
            nonlocal nlPreviousState
            nlPreviousState = lVT.PlaybackState
            lVT.PlaybackState = ePlaybackState.PAUSED
            lVT.seek(lFrameSlider.value())

        def _onSliderMoved(index: int):
            lVT.seek(lFrameSlider.value())

        def _onSliderRelease():
            lVT.seek(lFrameSlider.value())
            lVT.PlaybackState = nlPreviousState
        # endregion

        # Slider Events
        lFrameSlider.sliderPressed.connect(_onSliderPressed)
        lFrameSlider.sliderMoved.connect(_onSliderMoved)
        lFrameSlider.sliderReleased.connect(_onSliderRelease)

        lLoadButton.clicked.connect(_loadVideoFile)
        lPlayButton.clicked.connect(_playPause)
