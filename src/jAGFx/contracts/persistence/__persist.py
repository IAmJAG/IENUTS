from multiprocessing.queues import Queue

from ..serializer import iSerialisable


class iPersist(iSerialisable):  # noqa: N801
    @property
    def Lifeline(self) -> Queue: ...

    @property
    def PID(self) -> int: ...

    @property
    def UID(self) -> str: ...
