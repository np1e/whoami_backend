"""empty message

Revision ID: cff275376007
Revises: 21900959b179
Create Date: 2021-01-24 12:38:38.705096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cff275376007'
down_revision = '21900959b179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sid', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_column('sid')

    # ### end Alembic commands ###