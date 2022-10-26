import sys

from logsend import Output


class StdoutOutput(Output):
    def send(self, message):
        print(message)


class StderrOutput(Output):
    def send(self, message):
        print(message, file=sys.stderr)
