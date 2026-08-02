from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.organization_schema import (
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
    OrganizationResponseSchema,
)
from app.services.organization_service import OrganizationService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required

organization_bp = Blueprint("organizations", __name__)

create_schema = OrganizationCreateSchema()
update_schema = OrganizationUpdateSchema()

response_schema = OrganizationResponseSchema()
response_many_schema = OrganizationResponseSchema(many=True)


@organization_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_organizations():
    """Return all organizations."""

    organizations = OrganizationService.get_all()

    return success(
        data=response_many_schema.dump(organizations)
    )


@organization_bp.get("/<string:organization_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_organization(organization_id):
    """Return a single organization."""

    organization = OrganizationService.get_by_id(organization_id)

    return success(
        data=response_schema.dump(organization)
    )


@organization_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_organization():
    """Create a new organization."""

    data = create_schema.load(request.get_json())

    organization = OrganizationService.create(data)

    return success(
        message="Organization created successfully.",
        data=response_schema.dump(organization),
        status_code=201,
    )


@organization_bp.put("/<string:organization_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_organization(organization_id):
    """Update an existing organization."""

    data = update_schema.load(request.get_json())

    organization = OrganizationService.update(
        organization_id,
        data,
    )

    return success(
        message="Organization updated successfully.",
        data=response_schema.dump(organization),
    )


@organization_bp.delete("/<string:organization_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_organization(organization_id):
    """Delete an organization."""

    OrganizationService.delete(organization_id)

    return success(
        message="Organization deleted successfully."
    )