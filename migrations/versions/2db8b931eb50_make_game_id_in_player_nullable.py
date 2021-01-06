"""make game id in player nullable

Revision ID: 2db8b931eb50
Revises: 0237bca52b57
Create Date: 2021-01-06 12:38:11.594699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2db8b931eb50'
down_revision = '0237bca52b57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.alter_column('game_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.alter_column('game_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###