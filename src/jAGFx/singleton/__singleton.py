from collections.abc import Callable
from functools import wraps
from multiprocessing import RLock
from typing import Any

__all__ = ['SingletonC', 'SingletonF', 'SingletonM']


_classes: dict[type, int] = dict[type, int]()
_instances: dict[type, object] = dict[type, object]()
_instancesLock = RLock()
_DECORATOR_INIT_FLAG = '__isSingletonInitialized__'
_SINGLETON_CASCADING_FLAG = '__isCascadingSingleton__'

_SHM_NAME_NAME: str = "SHARENAMES"


def getClassHierarchyDepth(cls: type) -> int:
    lODepth: int = -1
    if cls in _classes:
        lODepth = _classes[cls]

    else:
        if hasattr(cls, _SINGLETON_CASCADING_FLAG):
            lODepth = 0
            _classes[cls] = lODepth
        else:
            for lBase in cls.__bases__:
                lDepth = getClassHierarchyDepth(lBase)

                if lDepth > 0:
                    _classes[cls] = lDepth + 1
                    lODepth = lDepth
                    break

    return lODepth

def getSingletonAncestors(cls: type, visited: set[type] | None = None) -> list[type]:
    if visited is None:
        visited = set()

    if cls in visited: return []

    visited.add(cls)

    lDecoratedAncestors: list[type] = []
    for lBase in reversed(cls.__mro__):  # Iterate from most base upwards
        if hasattr(lBase, _SINGLETON_CASCADING_FLAG):
            lDecoratedAncestors.append(lBase)
        lDecoratedAncestors.extend(getSingletonAncestors(lBase, visited))

    lSeen = set()
    lUniqueAncestors = [ancestor for ancestor in lDecoratedAncestors if not (ancestor in lSeen or lSeen.add(ancestor))]
    return lUniqueAncestors


class SingletonMP(type):
    SHM_NAMES: dict[str, type] = dict[str, type]()
    INSTANCES: dict[type, str] = dict[str, type]()
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class SingletonM(type):
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with _instancesLock:
            if cls not in _instances:
                instance = super().__call__(*args, **kwargs)
                _instances[cls] = instance
        return _instances[cls]

def SingletonF(cls: type) -> Callable[..., Any]:
    if not isinstance(cls, type): raise TypeError("Singleton decorator can only be applied to classes.")

    @wraps(cls)
    def getinstance(*args, **kwargs):
        with _instancesLock:
            if cls not in _instances:
                _instances[cls] = cls(*args, **kwargs)
            return _instances[cls]

    return getinstance

def SingletonC(cls: type) -> type:
    if not isinstance(cls, type):
        raise TypeError("Singleton decorator must be applied to a class.")

    setattr(cls, _DECORATOR_INIT_FLAG, False)

    lOrigInit = getattr(cls, '__init__', None)
    def __new__(klass, *args, **kwargs):
        if klass not in _instances:
            instance = object.__new__(klass)
            _instances[klass] = instance
        return _instances[klass]

    lWrapInit = lOrigInit
    if lOrigInit:
        @wraps(lOrigInit)
        def initWrapper(self, *args, **kwargs):
            lKlass = type(self)
            if getattr(lKlass, _DECORATOR_INIT_FLAG, False): return
            lOrigInit(self, *args, **kwargs)
            setattr(lKlass, _DECORATOR_INIT_FLAG, True)
        lWrapInit = initWrapper

    cls.__new__ = __new__  # type: ignore[assignment]
    if lWrapInit is not lOrigInit:
        cls.__init__ = initWrapper

    return cls

# def SingletonCascading(cls: type) -> type:
#     if not isinstance(cls, type):
#         raise TypeError("Singleton decorator must be applied to a class.")

#     lAncestors = getSingletonAncestors(cls)

#     if len(lAncestors) > 1:
#         raise TypeError(f"Invalid Cascading Singleton, has multiple cascading singleton ancestor")

#     if len(lAncestors) == 1:
#         lBaseAncestor = lAncestors[0]

#     else:
#         lBaseAncestor = cls

#     setattr(cls, _SINGLETON_CASCADING_FLAG, True)
#     setattr(cls, _DECORATOR_INIT_FLAG, False)

#     lOrigInit = getattr(cls, '__init__', None)
#     lOrigNew = getattr(cls, '__new__', None)

#     if not lOrigNew:
#         lOrigNew = lambda *args, **kwargs: object.__new__(*args, **kwargs)

#     def _getInit(oInit):
#         @wraps(lOrigInit)
#         def initWrapper(self, *args, **kwargs):
#             lKlass = type(self)
#             # check the class flag
#             if getattr(lKlass, _DECORATOR_INIT_FLAG, False): return

#             if oInit is not None and callable(oInit):
#                 oInit(self, *args, **kwargs)  # type: ignore

#             # update the class flag
#             setattr(lKlass, _DECORATOR_INIT_FLAG, True)

#         return initWrapper

#     def __new__(klass, *args, **kwargs):
#         with _instancesLock:

#             if lBaseAncestor not in _instances:
#                 if not hasattr(klass, _DECORATOR_INIT_FLAG):  # this is a subclass, _DECORATOR_INIT_FLAG is not readly defined unline the base cascading class
#                     lKOInit = getattr(klass, '__init__', None)

#                     setattr(klass, _DECORATOR_INIT_FLAG, False)
#                     setattr(klass, '__init__', _getInit(lKOInit))

#                 # Potential recursion here, potentially solve, by calling the old new instead of object.__new__(lBaseAncestor)
#                 lNewInstance = lOrigNew(*args, **kwargs)
#                 _instances[lBaseAncestor] = lNewInstance

#             # if klass is not the base anscestor and klass'es init flag is not set, create, copy, replace if most derived classed is class
#             if lBaseAncestor != klass:
#                 if not getattr(klass, _DECORATOR_INIT_FLAG, False):
#                     lInstance = _instances[lBaseAncestor]

#                     if klass is not type(lInstance):
#                         for attr, value in vars(lInstance).items():
#                             if not callable(value):
#                                 # if both instances has the same attribute, carry over the value
#                                 if hasattr(lNewInstance, attr):
#                                     setattr(lNewInstance, attr, value)

#                                 else:
#                                     # if the new instance does not have the attribute and new instance is not instance of klass, not the same heirarchy line
#                                     if not isinstance(lNewInstance, klass):
#                                         setattr(lNewInstance, attr, value)

#                                     # else attribute descrepancy must be retained, the descrepancy is unique to the new instanced - most derived class

#                         _instances[lBaseAncestor] = lNewInstance

#                     # else the instance
#                     if klass is not type(lInstance):
#                         if getClassHierarchyDepth(lNewInstance) > getClassHierarchyDepth(lInstance):
#                             lNewInstance = lNewInstance.__init__(*args, **kwargs)
#                             for attr, value in vars(lInstance).items():
#                                 if not callable(value):
#                                     # if both instances has the same attribute, carry over the value
#                                     if hasattr(lNewInstance, attr):
#                                         setattr(lNewInstance, attr, value)

#                                     else:
#                                         # if the new instance does not have the attribute and new instance is not instance of klass, not the same heirarchy line
#                                         if not isinstance(lNewInstance, klass):
#                                             setattr(lNewInstance, attr, value)

#                                         # else attribute descrepancy must be retaind, the descrepancy is unique to the new instanced - most derived class

#                             _instances[lBaseAncestor] = lNewInstance
#                 else:
#                     ...

#                     # else the instance stays the same

#             return _instances[lBaseAncestor]

#     lWrapInit = lOrigInit
#     if lOrigInit:
#         lWrapInit = _getInit(lOrigInit)

#     cls.__new__ = __new__
#     cls.__init__ = lWrapInit

#     return cls
