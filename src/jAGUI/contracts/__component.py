from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QWidget


class iComponent:
    @property
    def QN(self) -> str:
        return f"{type(self).__name__.upper()}.{self.Name.upper() if self.Name else ''}"

    @property
    def FQN(self) -> str:
        if self.Parent:
            if hasattr(self.Parent, "FQN"):
                return f"{self.Parent.FQN}.{self.QN}"
            else:
                return f"{type(self.Parent).__name__}.{self.QN}"

        return self.QN

    @property
    def Parent(self) -> QWidget: ...

    @Parent.setter
    def Parent(self, value: QWidget) -> None: ...

    @property
    def Name(self) -> str: ...

    @Name.setter
    def Name(self, value: str) -> None: ...

    @property
    def Settings(self) -> QSettings: ...
