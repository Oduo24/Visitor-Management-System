import uuid

from app.notifications.providers.email_provider import (
    EmailProvider,
)


class ConsoleEmailProvider(
    EmailProvider
):

    def send(
        self,
        recipient,
        subject,
        message,
    ):

        print(
            "\n"
            "========== EMAIL ==========\n"
            f"To: {recipient}\n"
            f"Subject: {subject}\n"
            "\n"
            f"{message}\n"
            "===========================\n"
        )

        return (
            f"console-email-{uuid.uuid4()}"
        )
