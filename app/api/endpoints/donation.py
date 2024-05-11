from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationUserDB
from app.services.invest import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    donate = await donation_crud.get_multi(session)
    return donate


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
    donations = await donation_crud.get_donations_by_user(
        user=user, session=session
    )
    return donations


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
        donate, session, user
    )
    await invest(new_donate, CharityProject, session)
    return new_donate
