import sqlalchemy as sqlalc
from sqlalchemy import orm

from backend import database as db


class Users(db.Base):
    __tablename__ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)
    hashed_password: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False, unique=True)
