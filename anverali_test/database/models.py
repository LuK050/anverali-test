from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from database import Base


class WomanName(Base):
    __tablename__: str = "names_woman"

    name: Mapped[str] = Column(String(32), primary_key=True)


class ManName(Base):
    __tablename__: str = "names_man"

    name: Mapped[str] = Column(String(32), primary_key=True)
