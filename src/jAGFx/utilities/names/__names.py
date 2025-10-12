import json
import random

from ...singleton import SingletonM

__all__ = ["_names"]


class _names(metaclass=SingletonM):
    def __init__(self):
        self._namesFileName = "./assets/names.json"
        self._names = self._loadNames()

    def _loadNames(self):
        lNames: dict[str, bool] = {}
        try:
            with open(self._namesFileName, "r") as lFile:
                lNames = json.load(lFile)

        except json.JSONDecodeError:
            with open(self._namesFileName, "r", encoding="utf-8-sig") as lFile:
                lNames = json.load(lFile)

            with open(self._namesFileName, "w") as lFile:
                json.dump(lNames, lFile)

        except Exception as ex:
            raise Exception("Unhandled exception from General Utilities") from ex

        finally:
            return {lName.strip(): lIUsed for lName, lIUsed in lNames.items()}

    def _saveNames(self):
        with open(self._namesFileName, "w") as lFile:
            json.dump(self._names, lFile, indent=4)

    def RandomNames(self, minLen: int = -1, maxLen: int = -1, trueName: bool = True):
        lName: str = ""
        minLen = minLen if minLen > 0 else 1
        maxLen = maxLen if maxLen > 0 else 32

        lMinMax = [minLen, maxLen]
        maxLen = max(lMinMax)
        minLen = min(lMinMax)

        def _getChoices() -> list[str]:
            return ""

        try:
            if trueName:
                lChoices: list[str] = list[str]()
                if minLen == 0:
                    for lNam, lIsUsed in self._names.items():
                            if len(lNam) >= maxLen and not lIsUsed and lName not in lChoices:
                                lChoices.append(lNam)
                else:
                    if len(self._names) > 0:
                        lChoices: list[str]
                        while len(lChoices) == 0:
                            for lNam, lIsUsed in self._names.items():
                                if len(lNam) >= minLen <= maxLen and not lIsUsed and lName not in lChoices:
                                    lChoices.append(lNam)

                if len(lChoices) > 0:
                    lName = random.choices(lChoices)[0]
                    self._names[lName] = True
                    self._saveNames()

            if lName == "":
                lPopConst = (
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                )
                lName = f"{(lambda: ''.join(random.choices(lPopConst, k=maxLen)))()}"

        except Exception as ex:
            raise Exception("Unhandled exception from General Utilities") from ex

        finally:
            return lName

    def SecureName(self, name: str):
        if name in self._names:
            lXName = self._names[name]
            self._names[name] = True

            if lXName is False:
                self._saveNames()

    def ResetNames(self):
        for lName in self._names:
            self._names[lName] = False
        self._saveNames()


# class _names(metaclass=SingletonM):
#     POPCONST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

#     def __init__(self):
#         self._manager = Manager()

#         self._namesFilename = "./assets/names.json"
#         self._names: dict[str, dict[str, int]] = self._manager.dict()
#         self._snames: dict[int, list[str]] = self._manager.dict()
#         self._fnames: dict[int, list[str]] = self._manager.dict()

#         self._snames[0] = self._manager.list()
#         self._snames[1] = self._manager.list()
#         self._fnames[0] = self._manager.list()
#         self._fnames[1] = self._manager.list()

#         self._usedNames: list[str] = self._manager.list()
#         self._ender: object = None
#         self._loadNames()

#         def _cleanup():
#             self._ender = None

#         atexit.register(_cleanup)

#     def _loadNames(self):
#         lNames: dict[str, dict[str, int]] = dict[str, dict[str, int]]()
#         try:
#             with open(self._namesFilename) as lFile:
#                 lNames = json.load(lFile)

#         except json.JSONDecodeError:
#             try:
#                 with open(self._namesFilename, encoding="utf-8") as lFile:
#                     lNames = json.load(lFile)

#                 self._saveNames()

#             except Exception as ex:
#                 raise Exception("Names file read error") from ex

#         except Exception as ex:
#             raise Exception("Names file read error") from ex

#         if not lNames:
#             raise Exception("Names is empty")

#         for lPart, lXNames in lNames.items():
#             lPart = lPart.strip()
#             if lPart not in self._names:
#                 self._names[lPart] = self._manager.dict()

#             lErrorOccured: bool = False
#             for lName, lValue in lXNames.items():
#                 try:
#                     self._names[lPart][lName.strip()] = lValue

#                 except Exception as ex:
#                     raise Exception("Error populating names") from ex
#                     lErrorOccured = True
#                     break

#                 if lPart == "firstnames":
#                     self._fnames[0].append(lName.strip())

#                 elif lPart == "surnames":
#                     self._snames[0].append(lName.strip())

#             if lErrorOccured:
#                 break

#         if self._fnames is None:
#             self._fnames = self._manager.dict()
#             self._fnames[0] = self._manager.list()
#             self._fnames[1] = self._manager.list()

#         if self._snames is None:
#             self._snames = self._manager.dict()
#             self._snames[0] = self._manager.list()
#             self._snames[1] = self._manager.list()

#         self._snames[0][:] = []
#         self._snames[1][:] = []
#         self._fnames[0][:] = []
#         self._fnames[1][:] = []

#         self._fnames[0].extend(list(self._names["firstnames"].keys()))
#         self._snames[0].extend(list(self._names["surnames"].keys()))

#     def _saveNames(self):
#         with open(self._namesFilename, "w") as lFile:
#             lNames: dict[str, dict[str, int]] = dict[str, dict[str, int]]()
#             for lNType, lXNames in self._names.items():
#                 if lNType not in lNames:
#                     lNames[lNType] = dict[str, int]()
#                 for lKey, lVal in lXNames.items():
#                     lNames[lNType][lKey.strip()] = lVal

#             json.dump(lNames, lFile)

#     def objectName(self, obj):
#         if hasattr(obj, "_name"):
#             obj._name = self.RandomNames()

#             def _objCleanName():
#                 lName: str = obj._name
#                 lSName, lFName = lName.split(",")
#                 if lName in self._usedNames:
#                     self._usedNames.remove(lName)
#                 self._names["firstnames"][lFName.strip()] -= 1
#                 self._names["surnames"][lSName.strip()] -= 1
#                 self._saveNames()

#             wref(obj, _objCleanName)

#     def RandomNames(self, trueName: bool = True, length: int = 12):
#         lName: str = ""
#         try:
#             if trueName:
#                 while True:
#                     if len(self._fnames[0]) == 0:
#                         self._fnames[0].extend(self._fnames[1])
#                         self._fnames[1][:] = []

#                     if len(self._snames[0]) == 0:
#                         self._snames[0].extend(self._snames[1])
#                         self._snames[1][:] = []
#                         if not self._snames[0]:
#                             break

#                     lFName: str = random.choice(list(self._fnames[0]))
#                     lSName: str = random.choice(list(self._snames[0]))

#                     lName = f"{lSName}, {lFName}"

#                     if lName not in self._usedNames:
#                         self._usedNames.append(lName)
#                         self._names["firstnames"][lFName] += 1
#                         self._names["surnames"][lSName] += 1
#                         self._saveNames()

#                         self._fnames[0].remove(lFName)
#                         self._fnames[1].append(lFName)

#                         self._snames[0].remove(lSName)
#                         self._snames[1].append(lSName)
#                         break

#             if lName == "":
#                 while lName in self._usedNames:
#                     lName = f"{(lambda: ''.join(random.choices(_names.POPCONST, k=length)))()}"

#                 self._usedNames.append(lName)
#             return lName

#         except Exception as ex:
#             raise Exception("Error generating random name") from ex

#     def ResetNames(self):
#         for lPart, lNames_dict_proxy in self._names.items():
#             for lName in list(lNames_dict_proxy.keys()):
#                 lNames_dict_proxy[lName.strip()] = 0

#         self._usedNames[:] = []

#         self._fnames[0][:] = list(self._names["firstnames"].keys())
#         self._fnames[1][:] = []
#         self._snames[0][:] = list(self._names["surnames"].keys())
#         self._snames[1][:] = []

#         self._saveNames()
