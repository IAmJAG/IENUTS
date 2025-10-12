import inspect

from ..types import isNone, isTypeAny
from .__signatures import signatures


def GenerateSignatures(sig: inspect.Signature) -> signatures:
    lSig: signatures = signatures()

    for lParam in sig.parameters.values():
        if lParam.name == "self":
            continue

        if lParam.annotation is inspect.Parameter.empty:
            # Allow empty annotations to be processed
            pass
        elif isTypeAny(lParam.annotation) or isNone(lParam.annotation):
            raise TypeError(
                f"Explicit type annotation required, got {lParam.annotation} at parameter {lParam.name}"
            )

        lSig.Add(lParam.name, lParam.annotation, lParam.kind)

    return lSig
