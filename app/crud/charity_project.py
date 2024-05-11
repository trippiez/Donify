from app.crud.base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject
from sqlalchemy import select
from typing import Optional


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


charity_project_crud = CRUDCharityProject(CharityProject)