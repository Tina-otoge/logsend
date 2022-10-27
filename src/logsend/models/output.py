from logsend.formatter import Formatter


class Output:
    skips_formatter = False

    formatter: Formatter = None

    def send(self, output: str):
        raise NotImplementedError
