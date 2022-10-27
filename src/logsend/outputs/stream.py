from dataclasses import dataclass

from logsend import Output
from logsend.models.entry import Entry
from logsend.streams import StreamsPool


@dataclass
class StreamOutput(Output):
    """
    Forwards received entries to every connected input streams with the same
    name
    """

    skips_formatter = True

    name: str

    def send(self, entry: Entry):
        StreamsPool.add_entry(self.name, entry)
