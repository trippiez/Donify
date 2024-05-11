from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import CharityProject
from app.crud.charity_project import charity_project_crud


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