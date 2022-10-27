from dataclasses import dataclass
from typing import Any

from logsend import Filter


@dataclass
class FieldFilter(Filter):
    path: str
    value: Any
    error_on_missing = True

    def check(self, entry):
        data = entry
        for key in self.path.split("/"):
            if not self.error_on_missing:
                if key not in data:
                    return False
            if isinstance(data, dict):
                data = data[key]
            else:
                data = getattr(data, key)
        return data == self.value
