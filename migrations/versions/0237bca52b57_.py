"""empty message

Revision ID: 0237bca52b57
Revises: ec17d8d22396
Create Date: 2021-01-06 11:59:45.717519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0237bca52b57'
down_revision = 'ec17d8d22396'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('name', sa.String(length=20), nullable=True))
    op.add_column('game', sa.Column('password_hash', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'password_hash')
    op.drop_column('game', 'name')
    # ### end Alembic commands ###
