from app.common.exceptions import NotFoundError

from app.repositories.host_repository import HostRepository


class HostService:

    @staticmethod
    def get_all():

        return HostRepository.get_all()

    @staticmethod
    def get_by_id(host_id):

        host = HostRepository.get_by_id(host_id)

        if not host:
            raise NotFoundError(
                "Host not found."
            )

        return host

    @staticmethod
    def search(query):

        return HostRepository.search(query)