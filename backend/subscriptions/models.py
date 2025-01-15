import fastcrud
import sqlalchemy as sqlalc
from sqlalchemy import orm

from backend import database as db


class Subscriptions(db.Base):
    __tablename__ = 'subscriptions'

    id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, primary_key=True, autoincrement=True)

    subscriber: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('users.id', ondelete='CASCADE'))
    subscription: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('users.id', ondelete='CASCADE'))

subscriptions_crud: fastcrud.FastCRUD = fastcrud.FastCRUD(Subscriptions)
