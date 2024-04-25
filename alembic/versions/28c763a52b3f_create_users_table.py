"""create users table

Revision ID: 28c763a52b3f
Revises: 
Create Date: 2024-04-19 16:15:17.854709

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '28c763a52b3f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uuid', sa.UUID, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50)),
        sa.Column('total', sa.Integer),
        sa.Column('wins', sa.Integer),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), server_onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
