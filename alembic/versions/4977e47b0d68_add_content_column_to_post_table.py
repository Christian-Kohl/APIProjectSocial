"""add content column to post table

Revision ID: 4977e47b0d68
Revises: c21a9c8c9bf9
Create Date: 2022-02-12 13:56:25.282634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4977e47b0d68'
down_revision = 'c21a9c8c9bf9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
