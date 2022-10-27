import typing

from logsend import Entry

if typing.TYPE_CHECKING:
    from logsend import StreamInput


class StreamsPool:
    _streams = {}

    @classmethod
    def register_input(cls, name, input: "StreamInput"):
        cls._streams.setdefault(name, [])
        cls._streams[name].append(input)

    @classmethod
    def add_entry(cls, name, entry: Entry):
        for stream in cls._streams.get(name, []):
            stream.add_entry(entry)
