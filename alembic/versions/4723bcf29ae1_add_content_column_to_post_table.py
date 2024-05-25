"""add content column to post table

Revision ID: 4723bcf29ae1
Revises: ae8eaeb02d21
Create Date: 2024-05-26 00:53:31.376225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4723bcf29ae1'
down_revision: Union[str, None] = 'ae8eaeb02d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
