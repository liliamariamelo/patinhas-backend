"""empty message

Revision ID: 22786148e799
Revises: 85c31770847c
Create Date: 2023-11-14 11:30:48.598019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22786148e799'
down_revision = '85c31770847c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animal', schema=None) as batch_op:
        batch_op.drop_column('vacina')

    with op.batch_alter_table('vacina', schema=None) as batch_op:
        batch_op.add_column(sa.Column('animal_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'animal', ['animal_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vacina', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('animal_id')

    with op.batch_alter_table('animal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vacina', sa.VARCHAR(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
