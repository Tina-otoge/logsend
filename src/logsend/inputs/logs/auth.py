from datetime import datetime

from logsend.inputs.file import FileInput as FileInput
from logsend.models.entry import Entry


class AuthLogInput(FileInput):
    DEFAULT_PATH = "/var/log/auth.log"

    class EntryClass(Entry):
        def __init__(self, message: str):
            prefix, message = message.split(": ", 1)
            words = prefix.split()
            self.time = datetime.strptime(" ".join(words[:3]), "%b %d %H:%M:%S")
            process = words[-1]
            if not "[" in process:
                process.strip("[]")
                pid = None
            else:
                pid = process[process.index("[") + 1 : process.index("]")]
                process = process[: -len(pid) - 2]
            hostname = words[-2]
            pid = int(pid)

            super().__init__(
                message=message,
                meta={
                    "pid": pid,
                    "process": process,
                    "hostname": hostname,
                },
            )
