
class Filter:
    def __init__(self, name: str, level: str):
        self._name = name
        self._level = level.upper()

    @property
    def Name(self):
        return self._name

    @property
    def Level(self):
        return self._level
