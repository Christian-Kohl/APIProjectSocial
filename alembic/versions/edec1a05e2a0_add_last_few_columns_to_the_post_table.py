"""add last few columns to the post table

Revision ID: edec1a05e2a0
Revises: aad0bf0d0f85
Create Date: 2022-02-12 14:11:13.810269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edec1a05e2a0'
down_revision = 'aad0bf0d0f85'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
