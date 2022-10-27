import argparse
import time
from pathlib import Path

import appdirs

from logsend.bridge import Bridge
from logsend.models.entry import Entry


def collect_bridges_files(paths):
    bridges_files = []
    for path in paths:
        path = Path(path)
        if not path.exists():
            print(f"Path {path} does not exist, skipping...")
            continue
        if path.is_dir():
            for file in path.rglob("**/*.yaml"):
                bridges_files.append(file)
            for file in path.rglob("**/*.yml"):
                bridges_files.append(file)
            continue
        if not path.suffix in (".yaml", ".yml"):
            print(f"Path {path} is not a YAML file, skipping...")
            continue
        bridges_files.append(path)
    return bridges_files


def loop(bridges, delay):
    while True:
        for bridge in bridges:
            bridge.run()
        time.sleep(delay)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bridges_path",
        help="Paths to bridges files or directories",
        default=[appdirs.user_config_dir("logsend", "logsend")],
        nargs="*",
    )
    parser.add_argument(
        "-d",
        "--delay",
        help="Delay between each run",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--show-hidden",
        action="store_true",
        help="Show hidden fields in logs",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any error",
    )
    args = parser.parse_args()
    if args.show_hidden:
        Entry.show_hidden = True
    bridges_files = collect_bridges_files(args.bridges_path)
    bridges = []
    for path in bridges_files:
        try:
            bridges.append(Bridge.from_file(path))
        except Exception as e:
            if args.strict:
                raise e
            print(f'Error while loading {path}: "{e}", skipping...')
    if not bridges:
        print("No bridges loaded, exiting...")
        return
    loop(bridges, args.delay)
