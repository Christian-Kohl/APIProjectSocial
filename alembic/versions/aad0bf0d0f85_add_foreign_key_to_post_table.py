"""Add foreign key to post table

Revision ID: aad0bf0d0f85
Revises: 1045cd251574
Create Date: 2022-02-12 14:06:55.609426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad0bf0d0f85'
down_revision = '1045cd251574'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
