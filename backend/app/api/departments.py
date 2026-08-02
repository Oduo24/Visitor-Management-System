from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.department_schema import (
    DepartmentCreateSchema,
    DepartmentUpdateSchema,
    DepartmentResponseSchema,
)
from app.services.department_service import DepartmentService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required

department_bp = Blueprint("departments", __name__)

create_schema = DepartmentCreateSchema()
update_schema = DepartmentUpdateSchema()

response_schema = DepartmentResponseSchema()
response_many_schema = DepartmentResponseSchema(many=True)


@department_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_departments():
    departments = DepartmentService.get_all()

    return success(
        data=response_many_schema.dump(departments)
    )


@department_bp.get("/<string:department_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_department(department_id):
    department = DepartmentService.get_by_id(
        department_id
    )

    return success(
        data=response_schema.dump(department)
    )


@department_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_department():
    data = create_schema.load(request.get_json())

    department = DepartmentService.create(data)

    return success(
        message="Department created successfully.",
        data=response_schema.dump(department),
        status_code=201,
    )


@department_bp.put("/<string:department_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_department(department_id):
    data = update_schema.load(request.get_json())

    department = DepartmentService.update(
        department_id,
        data,
    )

    return success(
        message="Department updated successfully.",
        data=response_schema.dump(department),
    )


@department_bp.delete("/<string:department_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_department(department_id):
    DepartmentService.delete(department_id)

    return success(
        message="Department deleted successfully."
    )