import fastcrud
import sqlalchemy as sqlalc
from sqlalchemy import orm

from backend import database as db


class UserCategories(db.Base):
    __tablename__ = 'user_categories'

    category_id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(sqlalc.String, nullable=False, unique=True)

    user: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('users.id', ondelete='CASCADE'))


class WishCategories(db.Base):
    __tablename__ = 'wish_categories'

    id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, primary_key=True, autoincrement=True)

    category_id: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('user_categories.category_id', ondelete='CASCADE'))
    wish: orm.Mapped[int] = orm.mapped_column(sqlalc.Integer, sqlalc.ForeignKey('wishes.id', ondelete='CASCADE'))

user_categories_crud: fastcrud.FastCRUD = fastcrud.FastCRUD(UserCategories)
wish_categories_crud: fastcrud.FastCRUD = fastcrud.FastCRUD(WishCategories)
