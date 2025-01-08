import sqlalchemy as sqlalc
from sqlalchemy import orm

from backend import database as db


class Wishes(db.Base):
    __tablename__ = 'wishes'

    id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)
    link: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)
    image: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)

    user: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('users.id'))
