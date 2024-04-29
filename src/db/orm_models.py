import uuid as pyuuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = 'users'

    uuid: Mapped[pyuuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    total: Mapped[int]
    wins: Mapped[int]
