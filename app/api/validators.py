from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.constants import FULLY_INVESTED_TRUE, ZERO_INVESTED_AMOUNT
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
):

    project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )

    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Благотворительный проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:

    project = await charity_project_crud.get(
        charity_project_id, session
    )

    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительный проект не найден!'
        )
    return project


async def check_full_amount_greater_than_invested(
    charity_project: CharityProject,
    obj_full_amount: int
):
    if charity_project.invested_amount > obj_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма пожертвования не может быть меньше внесённой!'
        )


async def check_project_not_fully_invested(
    charity_project: CharityProject
):
    if charity_project.fully_invested == FULLY_INVESTED_TRUE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Благотворительный проект полностью проинвестирован!'
        )


async def check_charity_project_invested_exists(
    charity_project: CharityProject
):
    if charity_project.invested_amount > ZERO_INVESTED_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Средства в благотворительный проект уже были внесены!'
        )