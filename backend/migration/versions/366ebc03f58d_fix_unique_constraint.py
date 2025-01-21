"""fix unique constraint

Revision ID: 366ebc03f58d
Revises: 5a7648aa726b
Create Date: 2025-01-21 15:16:01.398187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '366ebc03f58d'
down_revision: Union[str, None] = '5a7648aa726b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_categories_name_key', 'user_categories', type_='unique')
    op.create_unique_constraint('uix_name_category', 'user_categories', ['category_id', 'name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uix_name_category', 'user_categories', type_='unique')
    op.create_unique_constraint('user_categories_name_key', 'user_categories', ['name'])
    # ### end Alembic commands ###
