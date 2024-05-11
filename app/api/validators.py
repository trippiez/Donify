from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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
            status_code=422,
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
            status_code=404,
            detail='Благотворительный проект не найден!'
        )
    return project