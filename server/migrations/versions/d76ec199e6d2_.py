"""empty message

Revision ID: d76ec199e6d2
Revises: 0055ae904a55
Create Date: 2023-01-23 20:25:39.099725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd76ec199e6d2'
down_revision = '0055ae904a55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('room_name', sa.String(length=80), nullable=False))
        batch_op.add_column(
            sa.Column('player_sid', sa.String(), nullable=True))
        batch_op.create_unique_constraint('a', ['player_sid'])
        batch_op.create_unique_constraint('b', ['room_name'])
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('name', sa.VARCHAR(length=80), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('player_sid')
        batch_op.drop_column('room_name')

    # ### end Alembic commands ###