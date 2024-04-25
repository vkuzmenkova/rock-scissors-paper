import uuid as pyuuid

from sqlalchemy.orm import (DeclarativeBase, Mapped, joinedload, mapped_column,
                            relationship, scoped_session, sessionmaker)


class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = 'users'

    uuid: Mapped[pyuuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    total: Mapped[int]
    wins: Mapped[int]

# users_table = Table(
#     'users',
#     metadata,
#     Column("uuid", UUID, primary_key=True),
#     Column("username", String(50)),
#     Column("password", String(50)),
#     Column("total", Integer),
#     Column("wins", Integer),
# )
