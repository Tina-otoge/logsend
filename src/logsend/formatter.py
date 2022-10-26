from typing import Callable

from logsend.models.entry import Entry

Formatter = Callable[[Entry], str]
