from dataclasses import dataclass

import requests

from logsend import Output


@dataclass
class WebhookOutput(Output):
    MARKDOWN_CODE_BLOCK = False

    url: str

    def build_payload(self, message):
        return message

    def send(self, message):
        if self.MARKDOWN_CODE_BLOCK:
            message = f"```\n{message}\n```"
        requests.post(self.url, data=self.build_payload(message))
