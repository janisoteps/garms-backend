"""empty message

Revision ID: 56b39cda71b0
Revises: 05d4a598485c
Create Date: 2019-01-12 15:55:14.193981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56b39cda71b0'
down_revision = '05d4a598485c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_login', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'first_login')
    # ### end Alembic commands ###
