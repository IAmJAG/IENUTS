class iSerialisable:
    @property
    def Properties(self) -> list[str]:
        ...

    @classmethod
    def encode(cls) -> dict[str, object]:
        ...

    @classmethod
    def decode(cls, dct: dict[str, object]):
        ...

    def cleanUp(self): ...
