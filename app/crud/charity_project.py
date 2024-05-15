from typing import Optional, Union

from sqlalchemy import func, select
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
    ) -> list[dict[str, Union[str, int]]]:
        fundraising = (
            func.strftime('%s', CharityProject.close_date) -
            func.strftime('%s', CharityProject.create_date)
        )

        charity_projects = await session.execute(
            select([
                CharityProject.name,
                fundraising.label('fundraising'),
                CharityProject.description
            ]).where(
                CharityProject.fully_invested == 1
            ).order_by(fundraising)
        )
        charity_projects = charity_projects.all()
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)