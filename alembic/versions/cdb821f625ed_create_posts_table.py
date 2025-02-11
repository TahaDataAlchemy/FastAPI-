"""create posts table

Revision ID: cdb821f625ed
Revises: 
Create Date: 2025-02-04 07:53:32.867506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdb821f625ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column('title',sa.String,nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
