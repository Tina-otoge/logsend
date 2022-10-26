from .entry import Entry


class Filter:
    def check(self, entry: Entry):
        raise NotImplementedError
