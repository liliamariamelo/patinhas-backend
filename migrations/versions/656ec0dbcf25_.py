"""empty message

Revision ID: 656ec0dbcf25
Revises: fac202f28a33
Create Date: 2023-12-08 02:00:24.444018

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '656ec0dbcf25'
down_revision = 'fac202f28a33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.alter_column('nascimento',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.alter_column('nascimento',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)

    # ### end Alembic commands ###
