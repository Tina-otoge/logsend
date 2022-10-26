from dataclasses import dataclass

from logsend.outputs.webhook import WebhookOutput


@dataclass
class DiscordWebhookOutput(WebhookOutput):
    MARKDOWN_CODE_BLOCK = True

    url: str
    username: str = "Logsend"
    avatar_url: str = None

    def build_payload(self, message):
        return {
            "username": self.username,
            "avatar_url": self.avatar_url,
            "content": message,
        }
