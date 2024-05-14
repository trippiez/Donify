from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUserDB
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_donations_by_user(
        user=user, session=session
    )


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True
)
async def create_new_donation(
    donate: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donate = await donation_crud.create(
        donate, session, user, pass_commit=True
    )
    session.add_all(
        investing(
            new_donate,
            await charity_project_crud.get_unfinished_investments(session)))
    await session.commit()
    await session.refresh(new_donate)
    return new_donate
