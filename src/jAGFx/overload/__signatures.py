from copy import deepcopy
from inspect import Parameter, _ParameterKind
from itertools import permutations

from xxhash import xxh64

from ..types import isUnionType
from .__parameter import parameter


class signatures:
    def __init__(self):
        self._parameters: list[parameter] = []
        self._package: str | None = None
        self._module: str | None = None
        self._fid: int | None = None  # function/method Id

    @property
    def FunctionId(self) -> int | None:
        return self._fid

    @FunctionId.setter
    def FunctionId(self, fid: int):
        self._fid = fid

    @property
    def Length(self):
        return len(self._parameters)

    @property
    def Parameters(self):
        return self._parameters

    def Add(self, name: str, xtype: type, kind: _ParameterKind):
        self._parameters.append(parameter(name, xtype, kind))

    @property
    def HashStr(self):
        return "|".join([param.HashStr for param in self._parameters])

    @property
    def Hash(self):
        lHasher = xxh64()
        lHasher.update(self.HashStr.encode())
        return lHasher.digest().hex()

    def GenerateCombinations(self):
        lCombinations: dict[str, signatures] = {}

        def _addCombination(lNewSig: signatures):
            if lNewSig.Hash not in lCombinations:
                lCombinations.update({lNewSig.Hash: lNewSig})

        for i, param in enumerate(self.Parameters):
            if param.Kind == Parameter.POSITIONAL_ONLY:
                for kind in [Parameter.POSITIONAL_ONLY, Parameter.KEYWORD_ONLY]:
                    lNewSig: signatures = deepcopy(self)
                    lNewSig.Parameters[i] = parameter(param.Name, param.Type, kind)

                    # If the parameter is KEYWORD_ONLY, forces all succeeding parameters KEYWORD_ONLY
                    if kind == Parameter.KEYWORD_ONLY:
                        for j in range(i + 1, len(lNewSig.Parameters)):
                            lNewSig.Parameters[j] = parameter(
                                lNewSig.Parameters[j].Name,
                                lNewSig.Parameters[j].Type,
                                Parameter.KEYWORD_ONLY,
                            )

                        _addCombination(lNewSig)

                        # Generate all permutations of the KEYWORD_ONLY parameters
                        lKWOnlyParams = [
                            p
                            for p in lNewSig.Parameters
                            if p.Kind == Parameter.KEYWORD_ONLY
                        ]
                        if len(lKWOnlyParams) > 1:
                            for perm in permutations(lKWOnlyParams):
                                lPermSig = deepcopy(lNewSig)
                                lPermSig.Parameters[i:] = perm
                                _addCombination(lPermSig)
                        continue

                    _addCombination(lNewSig)
            else:
                _addCombination(self)

        else:
            _addCombination(self)

        return lCombinations.values()

    def __str__(self):
        return ",".join(
            [
                "union" if isUnionType(param.Type) else param.Type.__name__
                for param in self._parameters
            ]
        )

    def __repr__(self):
        return "-".join(
            {
                "union" if isUnionType(param.Type) else param.Type.__name__: param.Kind
                for param in self._parameters
            }
        )
