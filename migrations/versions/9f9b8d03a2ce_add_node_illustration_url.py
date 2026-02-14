"""add node illustration url

Revision ID: 9f9b8d03a2ce
Revises: 8b5d2f31ef10
Create Date: 2026-02-14 16:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f9b8d03a2ce'
down_revision = '8b5d2f31ef10'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('story_node', schema=None) as batch_op:
        batch_op.add_column(sa.Column('illustration_url', sa.String(length=500), nullable=True))


def downgrade():
    with op.batch_alter_table('story_node', schema=None) as batch_op:
        batch_op.drop_column('illustration_url')
