"""add last few columns to post table

Revision ID: f93c50835324
Revises: 419ca5a8047f
Create Date: 2025-11-12 16:03:33.469476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f93c50835324'
down_revision = '419ca5a8047f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
