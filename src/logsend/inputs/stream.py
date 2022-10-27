import time
from dataclasses import dataclass
from typing import Generator

from logsend import Entry, Input
from logsend.streams import StreamsPool


class GroupedEntry(Entry):
    def __init__(self, entries: list[Entry], sep: str):
        sep = bytes(sep, "utf-8").decode("unicode_escape")
        super().__init__(
            message=sep.join(str(x) for x in entries),
            meta={
                "_entries": entries,
                "_sep": sep,
            },
        )

    def __str__(self):
        return self.message


@dataclass
class StreamInput(Input):
    name: str
    delay_seconds: float = None
    max_chunk: int = None
    sep: str = "\n\n"

    def __post_init__(self):
        self._last_add = None
        self._queue = []
        self._buffer_enabled = self.delay_seconds is not None
        StreamsPool.register_input(self.name, self)

    def add_entry(self, entry: Entry):
        self._queue.append(entry)
        self._last_add = time.time()

    def poll(self) -> Generator[Entry, None, None]:
        if not self._queue:
            return
        if not self._buffer_enabled:
            yield from self._queue
            self._queue = []
            return
        if self._last_add is None:
            return
        now = time.time()
        delta = now - self._last_add
        if delta < self.delay_seconds:
            if self.max_chunk is None or len(self._queue) < self.max_chunk:
                return
        entry = GroupedEntry(self._queue, self.sep)
        self._queue = []
        yield entry
