import asyncio

from sqlalchemy import select, ReturnsRows

from bitrix import *
from database.database import AsyncSession, init_models
from database.models import WomanName, ManName
from enums import Gender


CONTACT_ID: int = 4


async def main():
    await init_models()

    contact: dict[str, Any] = await get_contact(CONTACT_ID)
    name: str = contact["NAME"]
    gender: str | None = None

    async with AsyncSession() as session:
        new_name = ManName(
            name="Кирилл"
        )
        session.add(new_name)
        await session.commit()

    async with AsyncSession() as session:
        stmt: ReturnsRows = select(ManName).where(ManName.name.ilike(name))
        result: ManName = (await session.execute(stmt)).first()

        if result:
            gender = Gender.MAN
        else:
            stmt: ReturnsRows = select(WomanName).where(WomanName.name.ilike(name))
            result: WomanName = (await session.execute(stmt)).first()

            if result:
                gender = Gender.WOMAN

    if gender is not None:
        await set_contact_gender(CONTACT_ID, gender)


if __name__ == "__main__":
    asyncio.run(main())
