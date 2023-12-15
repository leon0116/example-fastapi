"""empty message

Revision ID: 4b47ccdf615c
Revises: 8caf6836e9ea
Create Date: 2023-12-15 16:13:46.551904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b47ccdf615c'
down_revision: Union[str, None] = '8caf6836e9ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
