from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_invested_exists,
                                check_full_amount_greater_than_invested,
                                check_name_duplicate,
                                check_project_not_fully_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)

    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
        pass_commit=True)

    session.add_all(
        investing(
            new_charity_project,
            await donation_crud.get_unfinished_investments(session)))

    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_project_not_fully_invested(charity_project)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        await check_full_amount_greater_than_invested(
            charity_project, obj_in.full_amount
        )
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_charity_project_exists(charity_project_id, session)
    await check_charity_project_invested_exists(project)

    return await charity_project_crud.remove(project, session)