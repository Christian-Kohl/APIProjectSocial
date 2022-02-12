"""create post table

Revision ID: c21a9c8c9bf9
Revises: 
Create Date: 2022-02-12 13:50:46.892118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c21a9c8c9bf9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
