"""add unique contsraint

Revision ID: 68cb451e6f2c
Revises: 151cb3e88066
Create Date: 2024-04-25 16:29:56.239366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68cb451e6f2c'
down_revision: Union[str, None] = '151cb3e88066'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('unique_username_constraint', 'users', ['username'])

def downgrade() -> None:
    op.drop_constraint('unique_username_constraint', 'users')
