"""add content column to post table

Revision ID: 8d8d6850f362
Revises: cdb821f625ed
Create Date: 2025-02-05 18:13:43.685429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d8d6850f362'
down_revision: Union[str, None] = 'cdb821f625ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
