"""add users, votes table and update posts table

Revision ID: 5c02ef73fbaf
Revises: 4b47ccdf615c
Create Date: 2023-12-15 16:14:08.109830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c02ef73fbaf'
down_revision: Union[str, None] = '4b47ccdf615c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
