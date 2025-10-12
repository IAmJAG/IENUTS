from inspect import currentframe

from ..exceptions import jAGException
from .__signatures import signatures


class AmbiguityError(jAGException):
    def __init__(self, name: str, sigs: list[signatures], frame=None, *args, **kwargs):
        lConflictinSignatures = "\n\t".join([str(sig) for sig in sigs])
        message = f"Ambiguous call for '{name}'. Matching signatures:\n\t{lConflictinSignatures}"
        frame = currentframe().f_back if frame is None else frame  # type: ignore[reportOptionalMemberAccess]
        super().__init__(message, None, frame, *args, **kwargs)


class NoMatchingSignatureFound(jAGException):
    def __init__(
        self,
        name: str,
        origin: str,
        sigs: list[signatures],
        frame=None,
        *args,
        **kwargs,
    ):
        lSigStr = "\n\t".join([str(sig) for sig in sigs])
        message = f"No matching method found for call signature ({lSigStr}) in {origin}"
        frame = currentframe().f_back if frame is None else frame  # type: ignore[reportOptionalMemberAccess]
        super().__init__(message, None, frame, *args, **kwargs)
