from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission
from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.host_schema import HostResponseSchema
from app.services.host_service import HostService

host_bp = Blueprint(
    "hosts",
    __name__,
)

response_schema = HostResponseSchema()
response_many_schema = HostResponseSchema(
    many=True
)


@host_bp.get("")
@jwt_required()
@permission_required(Permission.HOST_READ)
def get_hosts():

    query = request.args.get("q")

    if query:
        hosts = HostService.search(query)
    else:
        hosts = HostService.get_all()

    return success(
        data=response_many_schema.dump(hosts)
    )


@host_bp.get("/<string:host_id>")
@jwt_required()
@permission_required(Permission.HOST_READ)
def get_host(host_id):

    host = HostService.get_by_id(
        host_id
    )

    return success(
        data=response_schema.dump(host)
    )