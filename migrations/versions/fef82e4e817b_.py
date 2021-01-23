"""empty message

Revision ID: fef82e4e817b
Revises: 3b1ef4b9152a
Create Date: 2021-01-22 10:17:47.149614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fef82e4e817b'
down_revision = '3b1ef4b9152a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('default', sa.Boolean(), nullable=True))
  
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collection', schema=None) as batch_op:
        batch_op.drop_column('default')

    # ### end Alembic commands ###