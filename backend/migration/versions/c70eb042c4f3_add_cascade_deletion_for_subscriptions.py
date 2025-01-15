"""add cascade deletion for subscriptions

Revision ID: c70eb042c4f3
Revises: cfb4a76aa65b
Create Date: 2025-01-15 14:04:54.773628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c70eb042c4f3'
down_revision: Union[str, None] = 'cfb4a76aa65b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('subscriptions_subscription_fkey', 'subscriptions', type_='foreignkey')
    op.drop_constraint('subscriptions_subscriber_fkey', 'subscriptions', type_='foreignkey')
    op.create_foreign_key(None, 'subscriptions', 'users', ['subscription'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'subscriptions', 'users', ['subscriber'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.create_foreign_key('subscriptions_subscriber_fkey', 'subscriptions', 'users', ['subscriber'], ['id'])
    op.create_foreign_key('subscriptions_subscription_fkey', 'subscriptions', 'users', ['subscription'], ['id'])
    # ### end Alembic commands ###
