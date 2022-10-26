from logsend.formatter import Formatter


class Output:
    formatter: Formatter = None

    def send(self, output: str):
        raise NotImplementedError
