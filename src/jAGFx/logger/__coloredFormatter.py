from copy import deepcopy
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Formatter
from re import finditer

from ..types import eAnsiColors, eLogLevel

DEFAULTLOGGERCOLORCODES: dict[str, dict[int, eAnsiColors]] = {
    "DEFAULT": {
        NOTSET: eAnsiColors.COLOR_WHITE,
        DEBUG: eAnsiColors.COLOR_BLUE,
        INFO: eAnsiColors.COLOR_GREEN,
        WARNING: eAnsiColors.COLOR_YELLOW,
        ERROR: eAnsiColors.COLOR_RED,
        CRITICAL: eAnsiColors.COLOR_BRIGHT_RED,
    }
}

FORMATTER = r"\{([^}]+?)}|\(([^)]+?)\)"


class ColoredFormatter(Formatter):
    def __init__(
        self,
        fmt="[{asctime}][{levelname:<8}] {message}",
        datefmt=None,
        style: str = "{",
        keyRegEx: str = FORMATTER,
        **kwargs,
    ) -> None:
        self._colorCodes: dict[str, dict[int, eAnsiColors]] = kwargs.pop(
            "colorCodes", DEFAULTLOGGERCOLORCODES
        )
        self._timefmt: str = kwargs.pop("timeformat", "%H%M%S%z")
        self._secondfmt: str = kwargs.pop("secformat", "%s %03d")

        super().__init__(fmt, datefmt, style, True, **kwargs)  # type: ignore
        self._originalFormat = deepcopy(self._style._fmt)
        self._styleKey = style
        self._regex = keyRegEx
        self._logLevelDict: dict[int, eLogLevel] = {
            lLevel.value: lLevel for lLevel in eLogLevel
        }

    @property
    def _match(self):
        return finditer(self._regex, deepcopy(self._originalFormat))

    @property
    def DefaultColorCodes(self):
        return self._colorCodes.get(
            "DEFAULT", DEFAULTLOGGERCOLORCODES.get("DEFAULT", {})
        )

    def _getColor(self, key: str, level: int):
        lColorCodes = self._colorCodes.get(key, self.DefaultColorCodes)
        lColor: eAnsiColors = lColorCodes.get(
            self._logLevelDict.get(level, eLogLevel.NOTSET).value,
            eAnsiColors.COLOR_WHITE,
        )
        return lColor.value

    def format(self, record):
        lFormat = deepcopy(self._originalFormat)
        try:
            lMatches = self._match

            for lMatch in lMatches:
                lFrmtKey: str = lMatch.group(0)
                lFrmtParts = lMatch.group(1).split(":")
                lKey = lFrmtParts[0].strip()

                lPadSpec = f":{lFrmtParts[1].strip()}" if len(lFrmtParts) > 1 else ""

                lColor = self._getColor(lKey, record.levelno)
                lNewFormat = (
                    f"{lColor}{{{lKey}{lPadSpec}}}{eAnsiColors.COLOR_RESET.value}"
                )

                lFormat = lFormat.replace(lFrmtKey, lNewFormat)

            self._style._fmt = lFormat

        except Exception as e:
            self._style._fmt = self._originalFormat
            raise e

        finally:
            result = super().format(record)

        return result
