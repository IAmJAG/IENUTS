from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class iAttributeValue(Protocol):
    @property
    def Key(self) -> str:
        ...

    @Key.setter
    def Key(self, value: str) -> None:
        ...

    @property
    def Value(self) -> Any:
        ...

    @Value.setter
    def Value(self, value: Any) -> None:
        ...

    def GenerateValue(self) -> Any:
        ...
