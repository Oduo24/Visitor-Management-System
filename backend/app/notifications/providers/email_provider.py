from abc import ABC, abstractmethod


class EmailProvider(ABC):

    @abstractmethod
    def send(
        self,
        recipient,
        subject,
        message,
    ):
        pass