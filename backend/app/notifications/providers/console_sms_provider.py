import uuid

from app.notifications.providers.sms_provider import (
    SMSProvider,
)


class ConsoleSMSProvider(
    SMSProvider
):

    def send(
        self,
        recipient,
        message,
    ):

        print(
            "\n"
            "=========== SMS ===========\n"
            f"To: {recipient}\n"
            "\n"
            f"{message}\n"
            "===========================\n"
        )

        return (
            f"console-sms-{uuid.uuid4()}"
        )