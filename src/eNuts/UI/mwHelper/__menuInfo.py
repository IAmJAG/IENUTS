from jAGUI.components import Button
from jAGUI.components.navigation import _navigationBar


class MenuInfo:
    def __init__(self, btn: Button, bar: _navigationBar, level: int, parentId: str) -> None:
        self._button: Button = btn
        self._childBar: _navigationBar = bar
        self._level: int = level
        self._parentId: str = parentId

    @property
    def Button(self) -> Button:
        return self._button

    @property
    def ChildBar(self) -> _navigationBar:
        return self._childBar

    @property
    def Level(self) -> int:
        return self._level

    @property
    def ParentId(self) -> str:
        return self._parentId
