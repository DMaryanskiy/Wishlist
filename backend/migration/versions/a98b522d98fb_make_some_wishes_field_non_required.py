"""make some wishes field non required

Revision ID: a98b522d98fb
Revises: c70eb042c4f3
Create Date: 2025-01-19 21:33:07.154479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a98b522d98fb'
down_revision: Union[str, None] = 'c70eb042c4f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('wishes', 'link',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('wishes', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('wishes', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('wishes_user_fkey', 'wishes', type_='foreignkey')
    op.create_foreign_key(None, 'wishes', 'users', ['user'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wishes', type_='foreignkey')
    op.create_foreign_key('wishes_user_fkey', 'wishes', 'users', ['user'], ['id'])
    op.alter_column('wishes', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('wishes', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('wishes', 'link',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
