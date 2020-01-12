"""empty message

Revision ID: 1c6cbf3cb20d
Revises: feeccb2ddccd
Create Date: 2019-12-17 11:09:05.460737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6cbf3cb20d'
down_revision = 'feeccb2ddccd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loading_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content_date', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loading_content')
    # ### end Alembic commands ###