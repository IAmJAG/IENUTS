import functools
import inspect
from collections.abc import Callable

from ..types import isUnionType
from .__exceptions import AmbiguityError, NoMatchingSignatureFound
from .__signatures import signatures
from .__utilities import GenerateSignatures

__all__ = ["OverloadDispatcher"]


class OverloadDispatcher:
    def __init__(self, func):
        self._originalFunction = func
        self._name = func.__name__
        self._overloads: dict[str, signatures] = {}
        self._methods: dict[int, Callable] = {}

        self._type = "FUNCTION" if func.__name__ == func.__qualname__ else "METHOD"
        try:
            lMod = func.__module__.split(".")
            self._package = ".".join(lMod[:-1])
            self._module = lMod[-1]

        except AttributeError:  # Handle built-ins or other callables without __module__
            self._package = ""
            self._module = ""

        self._class = (
            "" if self._type == "FUNCTION" else func.__qualname__.split(".")[0]
        )

        self.overload(func)
        functools.update_wrapper(self, self._originalFunction)

    @property
    def Class(self):
        return self._class

    @property
    def Module(self):
        return self._module

    @property
    def Package(self):
        return self._package

    @property
    def Name(self):
        return getattr(self, "__name__", self._name)

    def overload(self, func):
        lFId = id(func)

        if lFId not in self._methods:
            self._methods[lFId] = func

        try:
            lOSigs: signatures = GenerateSignatures(inspect.signature(func))

        except ValueError as ve:
            raise ValueError(
                f"Cannot overload function {func.__name__} with uninspectable signature."
            ) from ve

        lDuplicateSignatures: list[signatures] = []

        lSig: signatures
        for lSig in lOSigs.GenerateCombinations():
            if lSig.Hash not in self._overloads:
                lSig.FunctionId = lFId
                self._overloads[lSig.Hash] = lSig
            else:
                lExistingSig = self._overloads[lSig.Hash]
                if lExistingSig.FunctionId != lFId:
                    lDuplicateSignatures.append(lExistingSig)
                    lDuplicateSignatures.append(lSig)

        if len(lDuplicateSignatures) > 0:
            raise AmbiguityError(self.Name, list(set(lDuplicateSignatures)))

        return self

    def __call__(self, *args, **kwargs):
        lFunc = self._caller(*args, **kwargs)
        return lFunc(*args, **kwargs)

    def _caller(self, *args, **kwargs):
        lSignature = signatures()
        for i, arg in enumerate(args):
            lType = type(arg)
            lType = Callable if lType.__name__ == "function" else lType
            lSignature.Add(f"arg{i}", lType, inspect._ParameterKind.POSITIONAL_ONLY)  # type: ignore[reportArgumentType]

        for key, value in kwargs.items():
            lSignature.Add(key, type(value), inspect._ParameterKind.KEYWORD_ONLY)

        lFunc: Callable | None = self._matchSignature(lSignature)

        if lFunc is None:
            lLocation = f"{self.Package}.{self.Module}"
            if self.Class.strip() != "":
                lLocation += f".{self.Class}"
            raise NoMatchingSignatureFound(
                self.Name, f"{lLocation}.{self.Name}", [lSignature]
            )

        return lFunc

    def __get__(self, instance, owner):
        if instance is None:
            return self

        @functools.wraps(self._originalFunction)
        def wrapper(*args, **kwargs):
            lFunc = self._caller(*args, **kwargs)
            lBoundMethod = lFunc.__get__(instance, owner)
            return lBoundMethod(*args, **kwargs)

        return wrapper

    def _isSubclassOrUnionTypeSignatureMatch(
        self, overloadSig: signatures, callSig: signatures
    ) -> bool:
        if overloadSig.Length != callSig.Length:
            return False

        for overloadParam, callParam in zip(overloadSig.Parameters, callSig.Parameters):
            lOverloadType = overloadParam.Type
            lCallType = callParam.Type

            if lOverloadType == lCallType:
                continue

            if self._isSubClassOrUnion(lCallType, lOverloadType):
                continue
            else:
                return False

        return True

    def _isSubClassOrUnion(self, lCallType, lOverloadType) -> bool:
        try:
            if issubclass(lCallType, lOverloadType):
                return True
        except TypeError:
            pass

        if isUnionType(lOverloadType):
            lUnionMember = getattr(lOverloadType, "__args__", [])
            for lMemberType in lUnionMember:
                if lCallType == lMemberType:
                    return True
                try:
                    if issubclass(lCallType, lMemberType):
                        return True
                except TypeError:
                    continue
        return False

    def _matchSignature(self, sig: signatures):
        lSigMatch = self._overloads.get(sig.Hash, None)

        if lSigMatch is None:
            lMatches: dict[str, signatures] = dict[str, signatures]()
            for overload in self._overloads.values():
                if self._isSubclassOrUnionTypeSignatureMatch(overload, sig):
                    lMatches.update({overload.Hash: overload})

            if len(lMatches) > 1:
                lSigMatch = self._findBestMatch(lMatches, sig)
            elif len(lMatches) == 1:
                lSigMatch = next(iter(lMatches.values()))
                self._overloads[sig.Hash] = lSigMatch

        lMethod: Callable | None = None
        if lSigMatch is not None:
            lFunctionId = lSigMatch.FunctionId
            if lFunctionId is not None:
                lMethod = self._methods.get(lFunctionId, None)
                if lMethod is None:
                    raise LookupError(
                        f"Internal Error: Method ID {self.Name}:{lFunctionId} not found for signature {lSigMatch}"
                    )
            else:
                raise ValueError(
                    f"Internal Error: Matched signature {lSigMatch} has no FunctionId."
                )

        return lMethod

    def _findBestMatch(self, matches: dict[str, signatures], sig: signatures):
        lBestMatched = None
        lScore = 0
        lPrevScore = 0
        for lMatch in matches.values():
            lScore = 0
            for lParamIndex in range(len(lMatch.Parameters)):
                lScore += (
                    1
                    if lMatch.Parameters[lParamIndex].Kind
                    == sig.Parameters[lParamIndex].Kind
                    else 0
                )

            lBestMatched = lMatch if lScore >= lPrevScore else lBestMatched
            lPrevScore = lScore
        return lBestMatched
