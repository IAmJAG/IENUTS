from inspect import _ParameterKind

from xxhash import xxh64

from ..types import isUnionType


class parameter:
    def __init__(self, name: str, anon: type, kind: _ParameterKind):
        self._paramName: str = name
        self._paramType: type = anon
        # Forces parameters to be POSITIONAL_ONLY if the kind is POSITIONAL_OR_KEYWORD
        self._paramKind: _ParameterKind = (
            _ParameterKind.POSITIONAL_ONLY
            if kind == _ParameterKind.POSITIONAL_OR_KEYWORD
            else kind
        )
        self._hash: str | None = None

    @property
    def Name(self):
        return self._paramName

    @property
    def Type(self):
        return self._paramType

    @property
    def Kind(self):
        return self._paramKind

    @Kind.setter
    def Kind(self, kind: _ParameterKind):
        self._paramKind = kind

    @property
    def HashStr(self):
        lTypeName = "union" if isUnionType(self.Type) else self.Type.__name__
        if self.Kind == _ParameterKind.KEYWORD_ONLY:
            return f"{self.Name}:{lTypeName}-{self._paramKind.name}"

        return f"{lTypeName}-{self._paramKind.name}"

    @property
    def Hash(self):
        if self._hash is None:
            lHasher = xxh64()
            lHasher.update(self.HashStr.encode())
            self._hash = lHasher.digest().hex()
        return self._hash

    def __str__(self):
        return f"{self.Name}: {self.Type.__name__} - {self._paramKind.name}"

    def __repr__(self):
        return (
            f'"{self.Name}": {{\n\t{self.Type.__name__}\n\t{self._paramKind.name}\n}}'
        )
