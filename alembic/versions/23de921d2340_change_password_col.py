"""Change password col

Revision ID: 23de921d2340
Revises: 0867db1657e9
Create Date: 2022-06-16 14:52:05.633308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '23de921d2340'
down_revision = '0867db1657e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.String(length=128), nullable=False))
    op.drop_column('user', 'hash_pass')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hash_pass', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###