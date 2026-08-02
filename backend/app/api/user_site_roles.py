from flask import Blueprint, request

from app.common.responses import success

from app.schemas.user_site_role_schema import (
    UserSiteRoleCreateSchema,
    UserSiteRoleResponseSchema,
)

from app.services.user_site_role_service import (
    UserSiteRoleService,
)

user_site_role_bp = Blueprint(
    "user_site_roles",
    __name__,
)

create_schema = UserSiteRoleCreateSchema()

response_schema = UserSiteRoleResponseSchema()
response_many_schema = UserSiteRoleResponseSchema(
    many=True
)


@user_site_role_bp.get("")
def get_assignments():
    assignments = UserSiteRoleService.get_all()

    return success(
        data=response_many_schema.dump(assignments)
    )


@user_site_role_bp.get("/<string:assignment_id>")
def get_assignment(assignment_id):
    assignment = UserSiteRoleService.get_by_id(
        assignment_id
    )

    return success(
        data=response_schema.dump(assignment)
    )


@user_site_role_bp.post("")
def create_assignment():
    data = create_schema.load(
        request.get_json()
    )

    assignment = UserSiteRoleService.create(
        data
    )

    return success(
        message="Assignment created successfully.",
        data=response_schema.dump(assignment),
        status_code=201,
    )


@user_site_role_bp.delete("/<string:assignment_id>")
def delete_assignment(assignment_id):
    UserSiteRoleService.delete(
        assignment_id
    )

    return success(
        message="Assignment deleted successfully."
    )