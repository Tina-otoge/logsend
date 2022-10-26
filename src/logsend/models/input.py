from typing import Generator

from .entry import Entry


class Input:
    def poll(self) -> Generator[Entry, None, None]:
        raise NotImplementedError
