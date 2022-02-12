"""add user table

Revision ID: 1045cd251574
Revises: 4977e47b0d68
Create Date: 2022-02-12 13:59:53.137218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1045cd251574'
down_revision = '4977e47b0d68'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
