"""empty message

Revision ID: 2b077e6120b5
Revises: cb148933d9f5
Create Date: 2023-10-05 15:54:00.597235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b077e6120b5'
down_revision = 'cb148933d9f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacina')
    with op.batch_alter_table('animal', schema=None) as batch_op:
        batch_op.drop_column('vacina')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vacina', sa.VARCHAR(), autoincrement=False, nullable=False))

    op.create_table('vacina',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='vacina_pkey')
    )
    # ### end Alembic commands ###
