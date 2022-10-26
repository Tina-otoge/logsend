import dataclasses
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path

import yaml

from logsend.formatter import Formatter
from logsend.models.filter import Filter
from logsend.models.input import Input
from logsend.models.output import Output


@dataclass
class Bridge:
    inputs: list[Input]
    outputs: list[Output]
    formatter: Formatter = None
    filters: list[Filter] = dataclasses.field(default_factory=list)

    def run(self):
        for source in self.inputs:
            for entry in source.poll():
                for filter in self.filters:
                    if not filter.check(entry):
                        break
                for output in self.outputs:
                    formatter = output.formatter or self.formatter or str
                    output.send(formatter(entry))

    @staticmethod
    def _class_loader(cls_name: str, args: dict = None):
        cls = getattr(import_module("logsend"), cls_name)
        args = args or {}
        return cls(**args)

    @classmethod
    def from_file(cls, path: Path):
        with path.open() as f:
            data = yaml.safe_load(f)
        kwargs = {
            "inputs": [],
            "outputs": [],
        }
        for key in kwargs:
            for item in data.get(key, []):
                if isinstance(item, str):
                    item = {"type": item}
                name = item.pop("type") + key.title()[:-1]
                kwargs[key].append(cls._class_loader(name, item))
        if not kwargs["inputs"]:
            raise ValueError("No inputs defined")
        if not kwargs["outputs"]:
            raise ValueError("No outputs defined")
        bridge = cls(**kwargs)
        print(path, bridge)
        return bridge
