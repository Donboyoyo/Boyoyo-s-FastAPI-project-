"""add content column to posts table

Revision ID: 1b182130d0e5
Revises: 3c6cc7d0532e
Create Date: 2025-11-12 14:33:34.123203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b182130d0e5'
down_revision = '3c6cc7d0532e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
