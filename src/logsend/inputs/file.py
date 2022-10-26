import io

from logsend import Entry, Input


class FileInput(Input):
    DEFAULT_PATH = None
    EntryClass = Entry

    def __init__(self, path: str = None):
        if path is None:
            if self.DEFAULT_PATH is None:
                raise ValueError("No path provided")
            path = self.DEFAULT_PATH
        self.stream = open(path, "r")
        self.stream.seek(0, io.SEEK_END)

    def poll(self):
        for line in self.stream:
            yield self.EntryClass(message=line[:-1])
