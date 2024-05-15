from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )

        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        fundraising_in_days = func.juliandate(
            CharityProject.close_date
        ) - func.juliandate(
            CharityProject.create_date
        )

        charity_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1
            ).order_by(fundraising_in_days)
        )
        return charity_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)