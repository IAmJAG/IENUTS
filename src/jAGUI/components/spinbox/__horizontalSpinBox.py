from jAGUI.components.utilities import processMarker
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy, QWidget

from ..bases import ComponentBase


@processMarker(True, True)
class HorizontalSpinBox(ComponentBase):
    onValueChanged: Signal = Signal(int)
    def __init__(self, isreadonly: bool = True, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)
        self._minValue: int = 0
        self._maxValue: int = 99
        self._step: int = 1
        self._readOnly: bool = isreadonly

    @property
    def IsEditable(self) -> bool:
        return self._lineEdit.isReadOnly()

    @IsEditable.setter
    def IsEditable(self, value: bool):
        self._lineEdit.setReadOnly(value)

    def Load(self):
        super().Load()
        del self._readOnly

    def setupUI(self, layout: QBoxLayout | None = QHBoxLayout()):
        super().setupUI(layout)
        self._leftButton: QPushButton = QPushButton("◀")
        self._leftButton.clicked.connect(self._decrement)

        self._lineEdit: QLineEdit =  QLineEdit(str(0))
        self._lineEdit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self._lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.IsEditable = self._readOnly

        self._rightButton: QPushButton = QPushButton("▶")
        self._rightButton.clicked.connect(self._increment)

        self.Layout.addWidget(self._leftButton)
        self.Layout.addWidget(self._lineEdit)
        self.Layout.addWidget(self._rightButton)

        self._lineEdit.textChanged.connect(lambda newValue: self.onValueChanged.emit(int(newValue)))

    @property
    def Value(self) -> int:
        return int(self._lineEdit.text())

    @Value.setter
    def Value(self, value: int):
        lVal: int = max(self.MinimumValue, min(self._maxValue, value))
        self._lineEdit.setText(str(lVal))
        self._updateButtonState()

    @property
    def MinimumValue(self) -> int:
        return self._minValue

    @MinimumValue.setter
    def MinimumValue(self, value: int):
        self._minValue = value
        self.Value = int(self._lineEdit.text())
        self._updateButtonState()

    @property
    def MaximumValue(self) -> int:
        return self._maxValue

    @MaximumValue.setter
    def MaximumValue(self, value: int):
        self._maxValue = value
        self.Value = int(self._lineEdit.text())
        self._updateButtonState()

    @property
    def Step(self) -> int:
        return self._step

    @Step.setter
    def Step(self, value: int):
        self._step = value

    def _increment(self):
        self.Value += self.Step

    def _decrement(self):
        self.Value -= self.Step

    def _updateButtonState(self):
        self._leftButton.setEnabled(self.Value > self.MinimumValue)
        self._rightButton.setEnabled(self.Value < self.MaximumValue)

    def setRange(self, mini: int, maxi: int):
        self.MinimumValue = min(mini, maxi)
        self.MaximumValue = max(mini, maxi)
