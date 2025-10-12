from PySide6.QtWidgets import QBoxLayout, QWidget


def GetWidgetsParentLayout(wid: QWidget, layout: QBoxLayout = None) -> QBoxLayout:  #type: ignore
    if not isinstance(wid, QWidget):
        raise TypeError(f"Expecting QWidget got {type(wid).__name__}")

    if layout is None:
        lParent: QWidget = wid.parent()
        if not lParent.layout():
            raise Exception("Parent layout not avaialable.")

        layout = lParent.layout()

    for i in range(layout.count()):
        lItem = layout.itemAt(i)

        if lItem.widget() == wid:
            return layout

        if lItem.layout() is not None:
            return GetWidgetsParentLayout(wid, lItem.layout()) # type: ignore

    return None  # type: ignore

def findLayoutByName(layout: QBoxLayout, name: str) -> QBoxLayout:
    if layout is not None:
        if hasattr(layout, "objectName"):
            if layout.objectName().lower().strip() == name.lower().strip():
                return layout

    lResult = None
    if hasattr(layout, "count"):
        for i in range(layout.count()):
            lResult = findLayoutByName(layout.itemAt(i), name) # type: ignore
            if lResult is not None:
                break

    return lResult #type: ignore
