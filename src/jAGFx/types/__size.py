
class Size:
    def __init__(self, width: int = 0, height: int = 0) -> None:
        self._height: int = height
        self._width: int = width

    @property
    def Height(self) -> int:
        return self._height

    @Height.setter
    def Height(self) -> int:
        return self._height

    @property
    def Width(self) -> int:
        return self._width

    @Width.setter
    def Width(self) -> int:
        return self._width
