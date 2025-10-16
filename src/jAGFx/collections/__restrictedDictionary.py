
from ..exceptions import jAGException


class RestrictedDictionaryError(jAGException):
    """Custom exception for RestrictedDict."""
    def __init__(self):
        super().__init__("Invalid initialization: initData must be a dictionary.")


class RestrictedDictionary:
    def __init__(self, initData=None):
        if initData is not None and not isinstance(initData, dict):
            raise RestrictedDictionaryError("initData must be a dictionary")

        self._data = dict(initData) if initData is not None else {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"
