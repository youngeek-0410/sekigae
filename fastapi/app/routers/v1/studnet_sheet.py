from typing import List, Optional
from uuid import UUID

from app.api.v1 import StudentSheetAPI
from app.dependencies.auth import login_required
from app.models import StudentSheet
from app.schemas import (
    CreateFormStudentSheetSchema,
    ReadStudentSheetSchema,
    UpdateFormStudentSheetSchema,
)

from fastapi import APIRouter, Depends, Request

student_sheet_router = APIRouter()


@student_sheet_router.get(
    "/",
    response_model=List[ReadStudentSheetSchema],
    dependencies=[Depends(login_required)],
)
async def gets(request: Request) -> List[StudentSheet]:
    return StudentSheetAPI.gets(request)


@student_sheet_router.get(
    "/{uuid}",
    response_model=ReadStudentSheetSchema,
    dependencies=[Depends(login_required)],
)
async def get(request: Request, uuid: UUID) -> Optional[StudentSheet]:
    return StudentSheetAPI.get(request, uuid)


@student_sheet_router.post(
    "/", response_model=ReadStudentSheetSchema, dependencies=[Depends(login_required)]
)
async def create(
    request: Request, schema: CreateFormStudentSheetSchema
) -> StudentSheet:
    return StudentSheetAPI.create(request, schema)


@student_sheet_router.put(
    "/{uuid}",
    response_model=ReadStudentSheetSchema,
    dependencies=[Depends(login_required)],
)
async def update(
    request: Request,
    uuid: UUID,
    schema: UpdateFormStudentSheetSchema,
) -> StudentSheet:
    return StudentSheetAPI.update(request, uuid, schema)


@student_sheet_router.delete("/{uuid}", dependencies=[Depends(login_required)])
async def delete(request: Request, uuid: UUID) -> None:
    return StudentSheetAPI.delete(request, uuid)
