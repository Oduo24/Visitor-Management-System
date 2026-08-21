from abc import ABC, abstractmethod


class SMSProvider(ABC):

    @abstractmethod
    def send(
        self,
        recipient,
        message,
    ):
        pass
