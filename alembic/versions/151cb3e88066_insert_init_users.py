"""insert init users

Revision ID: 151cb3e88066
Revises: 28c763a52b3f
Create Date: 2024-04-19 16:17:40.084102

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '151cb3e88066'
down_revision: Union[str, None] = '28c763a52b3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO users (uuid, username, password, total, wins) VALUES" + 
               f"('{str(uuid.uuid4())}', 'jeeves', 'qwerty', 1, 0)," + 
               f"('{str(uuid.uuid4())}', 'wooster', 'qwerty1', 1, 1)"
    )


def downgrade() -> None:
    pass