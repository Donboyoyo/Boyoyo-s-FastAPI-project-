"""create posts table

Revision ID: 3c6cc7d0532e
Revises: 
Create Date: 2025-11-12 14:02:20.671381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c6cc7d0532e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                     sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                     sa.Column('title', sa.String(), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
