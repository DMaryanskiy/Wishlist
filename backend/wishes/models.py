import fastcrud
import sqlalchemy as sqlalc
from sqlalchemy import orm

from backend import database as db


class Wishes(db.Base):
    __tablename__ = 'wishes'

    id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False)
    link: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=True)
    description: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=True)
    image: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=True)

    user: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('users.id', ondelete='CASCADE'))

wishes_crud: fastcrud.FastCRUD = fastcrud.FastCRUD(Wishes)
