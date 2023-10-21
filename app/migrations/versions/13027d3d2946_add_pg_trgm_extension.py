"""Add pg_trgm extension

Revision ID: 13027d3d2946
Revises: 96e3c34b6a7a
Create Date: 2023-10-23 17:45:46.600825

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "13027d3d2946"
down_revision: Union[str, None] = "96e3c34b6a7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
    # ### end Alembic commands ###