from numbers import Number

from ..overload import OverloadDispatcher


def _clampValue(floor, ceiling, value):
    if floor >= ceiling:
        raise ValueError(f"Floor value ({floor}) must be less than ceiling value ({ceiling})")

    return max(floor, min(ceiling, value))

@OverloadDispatcher
def clampValue(floor: Number, ceiling: Number, value: Number) -> int:
    return _clampValue(floor, ceiling, value)


@clampValue.overload
def clampValue(floor: int, ceiling: int, value: int) -> int:
    return int(_clampValue(floor, ceiling, value))


@clampValue.overload
def clampValue(floor: float, ceiling: float, value: float) -> float:
    return float(_clampValue(floor, ceiling, value))
