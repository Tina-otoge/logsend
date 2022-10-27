import dataclasses
import enum
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Entry:
    show_hidden = False

    class Level(enum.Enum):
        DEBUG = enum.auto()
        INFO = enum.auto()
        WARNING = enum.auto()
        ERROR = enum.auto()
        CRITICAL = enum.auto()

    message: str
    meta: dict[str, str] = dataclasses.field(default_factory=dict)
    time: datetime = dataclasses.field(default_factory=datetime.utcnow)
    level: Level = None

    def __str__(self):
        parts = []
        parts.append(self.time.isoformat())
        if self.level:
            parts.append(f"[{self.level.name}]")
        parts.append(self.message)
        if self.meta:
            parts.append(
                json.dumps(
                    {
                        k: v
                        for k, v in self.meta.items()
                        if not k.startswith("_") or self.show_hidden
                    },
                    indent=2,
                    default=str,
                )
            )
        return " ".join(parts)
