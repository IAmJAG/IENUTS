# ==================================================================================
import json
import os

# ==================================================================================
from typing import Optional

# ==================================================================================
from jAGFx.contracts.configuration import iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import debug
from jAGFx.overload import OverloadDispatcher
from jAGFx.serializer import Serialisable, jsonDecode

# ==================================================================================
from proto import iTag


class TagCollection(Serialisable, list):
    @OverloadDispatcher
    def __init__(self) -> None:
        if hasattr(self, "_usedCodes") and hasattr(self, "_usedTexts"):
            # init has been called once already, do not reinitialize
            return

        super().__init__()

        self._usedCodes: set[int] = set()
        self._usedTexts: set[str] = set()

    @__init__.overload
    def __init__(self, dct: dict) -> None:
        self.decode(dct)

    @__init__.overload
    def __init__(self, tags: list) -> None:
        self.__init__()
        for lTag in tags:
            try:
                lDecodedTag: iTag = jsonDecode(lTag)
                self.Append(lDecodedTag)

            except KeyError as ke:
                debug(f"Skipping invalid tag: {lTag}\n({ke})", err=ke)

            except Exception as ex:
                debug(f"Skipping invalid tag: {lTag}", err=ex)

    @__init__.overload
    def __init__(self, tags: tuple) -> None:
        self.__init__(list(tags))

    def Append(self, tag: iTag) -> None:
        super().append(tag)
        self._usedCodes.add(tag.Code)
        self._usedTexts.add(tag.Text.lower())

    def Remove(self, tag: iTag) -> None:
        if tag in self:
            super().remove(tag)
            self._usedCodes.discard(tag.Code)
            self._usedTexts.discard(tag.Text.lower())

    def Clear(self) -> None:
        super().clear()
        self._usedCodes.clear()
        self._usedTexts.clear()

    def encode(self) -> dict[str, object]:
        lDict: dict = super().encode()
        lDict["Tags"] = [lTag.encode() for lTag in self]
        return lDict

    def _encodeProperty(self, prop: str):
        if prop == "Tags":
            return [tag.encode() for tag in self], False

        return super()._encodeProperty(prop)

    def FindByCode(self, code: int) -> Optional[iTag]:
        """Find a tag by its exact code."""
        for lTag in self:
            if lTag.Code == code:
                return lTag
        return None

    def FindByText(self, text: str, caseSensitive: bool = False) -> list[iTag]:
        """Find tags containing the specified text in their Text property."""
        lResults: list[iTag] = []
        lSearchText = text if caseSensitive else text.lower()

        for lTag in self:
            lTagText = lTag.Text if caseSensitive else lTag.Text.lower()
            if lSearchText in lTagText:
                lResults.append(lTag)

        return lResults

    def FilterByDescription(self, keyword: str, caseSensitive: bool = False) -> list[iTag]:
        """Filter tags by keyword in their Description property."""
        lResults: list[iTag] = []
        lSearchKeyword = keyword if caseSensitive else keyword.lower()

        for lTag in self:
            lDescription = lTag.Description if caseSensitive else lTag.Description.lower()
            if lSearchKeyword in lDescription:
                lResults.append(lTag)

        return lResults

    def GetTagsWithCodes(self, codes: list[int]) -> list[iTag]:
        """Get tags that match any of the provided codes."""
        lResults: list[iTag] = []
        lCodeSet = set(codes)

        for lTag in self:
            if lTag.Code in lCodeSet:
                lResults.append(lTag)

        return lResults

    def decode(self, lDict: dict) -> None:
        lModule: list[str] = self.__module__.split(".")
        if lModule[len(lModule) - 1].startswith("__"):
            lModuleStr: str = ".".join(lModule[:-1])
        else:
            lModuleStr: str = ".".join(lModule)

        if lDict["__type__"].strip() == f"{lModuleStr}.{type(self).__name__}".strip():
            try:
                if hasattr(self, "_usedCodes") and hasattr(self, "_usedTexts"):
                    self.Clear()

                if "Tags" in lDict:
                    self.__init__(lDict["Tags"])
                return
            except KeyError:
                raise Exception("Invalid data provided!")

        else:
            raise Exception(f"Invalid entity class, expecting a {lModuleStr}.{type(self).__name__} got {lDict['__type__']}")
