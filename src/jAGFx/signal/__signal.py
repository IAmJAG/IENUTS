import inspect
import queue
from collections.abc import Callable
from threading import Event, RLock, Thread
from typing import Any, Optional, Tuple, get_type_hints
from weakref import ref as wref

from jAGFx.logger import warning
from jAGFx.utilities.names import getRandomNames

from ..exceptions import invalidParameterTypeException, jAGException
from ..types import Is


class Signal:
    def __init__(self, *args: type):
        self._args: Tuple[type, ...] = args
        self._slotLock: RLock = RLock()
        self._slots: dict[Callable[..., Any], tuple[bool, int]] = {}
        self._listenerSlots: dict[Callable[..., Any], tuple[bool, int]] = {}  # Lock-free copy for listener
        self._queue = queue.Queue(maxsize=1000)  # Add max size to prevent memory issues
        self._listenerThread: Optional[Thread] = None
        self._stopEvent = Event()
        self._name: str = getRandomNames(4, 8)
        self._emitCount: int = 0  # For monitoring

        wref(self, self._cleanup)

    def connect(self, slot: Callable[..., Any], blocking: bool = False, priority: int = 0):
        if not callable(slot):
            raise invalidParameterTypeException(Callable[..., Any], type(slot), "Error connecting...")

        lSlotHints = get_type_hints(slot)
        lSlotArgs = tuple(
            lSlotHints.get(param.name)
            for param in inspect.signature(slot).parameters.values()
            if param.kind not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
        )

        if self._args:
            if len(lSlotArgs) != len(self._args):
                warning(
                    f"{type(self).__name__}.{self.Name}: Argument count mismatch!",
                    TypeError(f"Slot expects {len(lSlotArgs)} arguments, signal expects {len(self._args)}."),
                )

            for lSignalArgType, lSlotArgType in zip(self._args, lSlotArgs):
                if lSlotArgType is None:
                    continue
                if not Is(lSlotArgType, lSignalArgType):
                    raise jAGException(
                        f"{type(self).__name__}.{self.Name}: Argument type mismatch!",
                        TypeError(f"Slot argument type '{lSlotArgType}' is not compatible with signal argument type '{lSignalArgType}'."),
                    )

        with self._slotLock:
            self._slots[slot] = (blocking, priority)
            self._listenerSlots = self._slots.copy()  # Update lock-free copy

        if not (self._listenerThread and self._listenerThread.is_alive()):
            self._startListening()

    def isConnected(self, slot: Callable[..., Any]) -> bool:
        if slot is None:
            return False

        with self._slotLock:
            return slot in self._slots

    def disconnect(self, slot: Callable[..., Any]):
        with self._slotLock:
            self._slots.pop(slot, None)
            self._listenerSlots = self._slots.copy()  # Update lock-free copy

    def disconnectAll(self):
        with self._slotLock:
            self._slots.clear()
            self._listenerSlots = self._slots.copy()  # Update lock-free copy

    def emit(self, *args: Any):
        if self._args and len(args) != len(self._args):
            raise jAGException(f"{type(self).__name__}.{self.Name}: Emitted {len(args)} arguments, expected {len(self._args)}.")

        if self._args:
            for lEmittedArg, lExpectedType in zip(args, self._args):
                if isinstance(lEmittedArg, lExpectedType):
                    continue
                if lExpectedType is not any and not Is(lEmittedArg, lExpectedType):
                    raise jAGException(
                        f"{type(self).__name__}.{self.Name}: Emitted argument of type '{type(lEmittedArg).__name__}' is not compatible with expected type '{lExpectedType}'."
                    )

        with self._slotLock:
            # Sort slots by priority (higher first) for consistent execution order
            lSortedSlots = sorted(self._slots.items(), key=lambda x: x[1][1], reverse=True)
            for slot, (blocking, _) in lSortedSlots:
                if blocking:
                    try:
                        slot(*args)

                    except Exception as e:
                        # Log error but continue processing other slots
                        warning(f"Exception in blocking slot for {self.Name}", e)
                        continue

                else:
                    try:
                        self._queue.put((args, slot), timeout=0.1)  # Add timeout to prevent blocking
                    except queue.Full:
                        warning(f"Signal queue full for {self.Name}, dropping slot execution")
                        continue

        self._emitCount += 1

        if not self._queue.empty() and (self._listenerThread is None or not self._listenerThread.is_alive()):
            self._startListening()

    def _listener(self):
        while not self._stopEvent.is_set():
            try:
                lArgs, lSlot = self._queue.get(timeout=1.0)  # Use reasonable timeout
                # Use lock-free copy for high-performance reads
                if lSlot in self._listenerSlots:  # Check if slot is still connected (lock-free)
                    try:
                        lSlot(*lArgs)

                    except Exception as e:
                        warning(f"Exception in non-blocking slot for {self.Name}", e)
                        # Continue processing other items instead of crashing

                self._queue.task_done()

            except queue.Empty:
                continue

    def _startListening(self):
        with self._slotLock:
            if self._listenerThread is None or not self._listenerThread.is_alive():
                self._stopEvent.clear()
                self._listenerThread = Thread(target=self._listener, daemon=True, name=f"Signal-{self._name}")
                self._listenerThread.start()

    def _cleanup(self, _):
        self._stopEvent.set()
        if self._listenerThread is not None and self._listenerThread.is_alive():
            self._listenerThread.join(timeout=1.0)
            self._listenerThread = None

    @property
    def Name(self) -> str:
        return self._name

    @property
    def EmitCount(self) -> int:
        return self._emitCount

    @property
    def ConnectedSlotsCount(self) -> int:
        with self._slotLock:
            return len(self._slots)
