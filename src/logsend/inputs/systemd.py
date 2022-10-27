from systemd import journal

from logsend import Entry, Input


class SystemdEntry(Entry):
    def __init__(self, journal_log):
        super().__init__(
            time=journal_log["__REALTIME_TIMESTAMP"],
            message=journal_log["MESSAGE"],
            meta={
                "unit": journal_log.get("_SYSTEMD_UNIT"),
                "id": journal_log.get("SYSLOG_IDENTIFIER"),
                "_raw": journal_log,
            },
        )


class SystemdInput(Input):
    def __init__(self):
        self.journal = journal.Reader()
        self.journal.seek_tail()
        for _ in self.journal:
            # Seek to the end of the journal
            pass

    def poll(self):
        for entry in self.journal:
            yield SystemdEntry(entry)
