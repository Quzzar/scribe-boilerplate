from slack_sdk.webhook import WebhookClient
import os
import linecache
import sys

URL_MAP = {
    "eng-scribe": "https://hooks.slack.com/services/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",
}

def send_slack_message(message: str, webhook_urls: list, blocks: any = []):
    if (
        os.environ.get("FLASK_ENV") != "development"#"production"
    ):
        return

    for url in webhook_urls:
        webhook = WebhookClient(url)
        webhook.send(text=message, blocks=blocks)

    return True
