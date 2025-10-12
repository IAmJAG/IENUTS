from jAGFx.overload import OverloadDispatcher


@OverloadDispatcher
def convertSquareSides(values: list[int]):
    lLeft, lTop, lRight, lBottom = [0, 0, 0, 0]

    if isinstance(values, list):
        lLen = len(values)
        if lLen == 1:
            lLeft, lTop, lRight, lBottom = values[0], values[0], values[0], values[0]

        elif lLen == 2:
            lLeft, lRight = values[0], values[0]
            lTop, lBottom = values[1], values[1]

        elif lLen == 4:
            lLeft, lTop, lRight, lBottom = values

        else:
            raise ValueError("Square list must have 1, 2, or 4 elements")

    return lLeft, lTop, lRight, lBottom


@convertSquareSides.overload
def convertSquareSides(values: tuple[int]):
    if isinstance(values, tuple):
        return convertSquareSides(list(values))


@convertSquareSides.overload
def convertSquareSides(value: int):
    return value, value, value, value
