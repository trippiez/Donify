from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invested_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
):
    objects = await session.execute(
        select(obj_in).where(
            obj_in.fully_invested == 0
        ).order_by(obj_in.create_date)
    )
    return objects.scalars().all()


async def close_date_object(
    obj_in: Union[CharityProject, Donation]
):
    obj_in.invested_amount = obj_in.full_amount
    obj_in.close_date = datetime.now()
    obj_in.fully_invested = True
    return obj_in


async def invest(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
):
    remainder_in = obj_in.full_amount - obj_in.invested_amount
    remainder_model = obj_model.full_amount - obj_model.invested_amount

    if remainder_in > remainder_model:
        obj_in.invested_amount += remainder_model
        await close_date_object(obj_model)
    elif remainder_in == remainder_model:
        await close_date_object(obj_in)
        await close_date_object(obj_model)
    else:
        obj_model.invested_amount += remainder_in
        await close_date_object(obj_in)

    return obj_in, obj_model


async def investing(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
    session: AsyncSession
):
    objects = await get_not_full_invested_objects(obj_model, session)

    for obj in objects:
        obj_in, obj_model = await invest(obj_in, obj)
        session.add(obj_in)
        session.add(obj)

    await session.commit()
    await session.refresh(obj_in)
    return obj_in