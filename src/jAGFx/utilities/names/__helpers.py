from .__names import _names

__all__ = ["getRandomNames", "name", "resetNames"]


def getRandomNames(length: int = 12, trueName: bool = True):
    lGen: _names = _names()
    return lGen.RandomNames(trueName, length)


def resetNames():
    lGen: _names = _names()
    lGen.ResetNames()


def name(obj):
    lGen: _names = _names()
    lGen.objectName(obj)
