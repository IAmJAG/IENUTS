# ------------------------------------------------------
from functools import wraps
from inspect import currentframe
from typing import Any

# ------------------------------------------------------
from jAGFx.logger import error, info, warning
from jAGFx.property import Property
from PySide6.QtCore import Signal

__all__ = ["processMarker", "propertyChange"]


def propertyChange(cls):
    if not hasattr(cls, "OnPropertyChanging"):
        cls.OnPropertyChanging = Signal(Any, str, bool, bool)

    if not hasattr(cls, "OnPropertyChanged"):
        cls.OnPropertyChanged = Signal(Any, str, bool, bool)

    return cls


def infoStart(currentFrame=None):
    currentFrame = currentFrame if currentFrame else currentframe()
    info(f"{currentFrame.f_code.co_name} from {currentFrame.f_globals['__name__']}")


def infoEnd(currentFrame=None):
    currentFrame = currentFrame if currentFrame else currentframe()
    info(f"{currentFrame.f_code.co_name} from {currentFrame.f_globals['__name__']}")


def _addProperties(cls):
    @Property
    def IsInitialized(self) -> bool:
        return self._isinitialized

    @Property
    def IsUIInitialized(self) -> bool:
        return self._isuiinitialized

    @Property
    def IsLoaded(self) -> bool:
        return self._isloaded

    cls.IsInitialized = IsInitialized
    cls.IsUIInitialized = IsUIInitialized
    cls.IsLoaded = IsLoaded
    return cls


def _installPropertySignals(cls, UIAfterInit, LoadAfterUI):
    cls = propertyChange(cls)

    def _OnPropertyChanged(instance, propName: str, old: bool, new: bool):
        IsMe = type(instance) is cls
        if IsMe and new and (UIAfterInit or LoadAfterUI):
            if propName == "IsInitialized" and UIAfterInit:
                if hasattr(instance, "setupUI"):
                    instance.setupUI()

            elif propName == "IsUIInitialized" and LoadAfterUI:
                if hasattr(instance, "Load"):
                    instance.Load()

    lOldInit = cls.__init__

    @wraps(lOldInit)
    def _xNewInit(instance, *args, **kwargs):
        lResult = lOldInit(instance, *args, **kwargs)
        instance.OnPropertyChanged.connect(_OnPropertyChanged)
        return lResult

    cls.__init__ = _xNewInit
    return cls


def _getNewPro(cls, methName: str, propName: str):
    lOldMethod = getattr(cls, methName, None)
    if lOldMethod is None:
        warning(f"Replacing method, {methName} not found.")
        return None

    @wraps(lOldMethod)
    def newPro(instance, *args, **kwargs):
        cFrame = currentframe().f_back  # type: ignore
        infoStart(cFrame)
        IsMe = type(instance) is cls
        lIsInit = getattr(instance, f"_{propName.lower()}", False)
        if lIsInit:
            info(f"{methName} already executed, skipping...")
            return
        result = None

        if lOldMethod:
            result = lOldMethod(instance, *args, **kwargs)

        if IsMe:
            info(f"Setting {propName} to {IsMe}")
            setattr(instance, f"_{propName.lower()}", IsMe)
            instance.OnPropertyChanged.emit(instance, propName, False, True)
        infoEnd(cFrame)
        return result

    return newPro


def _replaceMethods(cls, lProNames):
    for lMethName, lProName in lProNames:
        try:
            new_method = _getNewPro(cls, lMethName, lProName)
            if new_method:
                setattr(cls, lMethName, new_method)
        except Exception as e:  # noqa: PERF203
            error(f"Error replacing method {lMethName}.", e)
    return cls


def _replaceNew(cls, lProNames):
    lOldNew = cls.__new__

    @wraps(lOldNew)
    def _newNew(cls_, *args, **kwargs):
        instance = lOldNew(cls_)
        if isinstance(instance, cls_):
            for _, lProName in lProNames:
                setattr(instance, f"_{lProName.strip().lower()}", False)
        return instance

    cls.__new__ = _newNew
    return cls


def processMarker(UIAfterInit: bool = False, LoadAfterUI: bool = False):
    def decorator(cls):
        lProNames: list[tuple[str, str]] = [
            ("__init__", "IsInitialized"),
            ("setupUI", "IsUIInitialized"),
            ("Load", "IsLoaded"),
        ]
        cls = _addProperties(cls)
        if UIAfterInit or LoadAfterUI:
            cls = _installPropertySignals(cls, UIAfterInit, LoadAfterUI)
        cls = _replaceMethods(cls, lProNames)
        cls = _replaceNew(cls, lProNames)
        return cls

    return decorator
