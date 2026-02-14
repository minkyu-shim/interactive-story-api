"""add choice roll fields

Revision ID: 8b5d2f31ef10
Revises: ed712c1ab000
Create Date: 2026-02-14 15:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b5d2f31ef10'
down_revision = 'ed712c1ab000'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('choice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requires_roll', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('roll_sides', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('roll_required', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('on_fail_target_node_custom_id', sa.String(length=50), nullable=True))


def downgrade():
    with op.batch_alter_table('choice', schema=None) as batch_op:
        batch_op.drop_column('on_fail_target_node_custom_id')
        batch_op.drop_column('roll_required')
        batch_op.drop_column('roll_sides')
        batch_op.drop_column('requires_roll')
