from PySide6.QtWidgets import QBoxLayout, QWidget

from .__component import Component


class ComponentBase(Component, QWidget):
    def __init__(self, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)

    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
