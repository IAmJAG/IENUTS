from .__tsList import TSList


class Buffer(TSList):
    def __init__(self, maxSize: int):
        super().__init__()
        self._maxSize = maxSize

    def append(self, item):
        if len(self) >= self._maxSize:
            self.pop(0)
        super().append(item)

    @property
    def MaximumSize(self):
        return self._maxSize
