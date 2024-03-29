"""empty message

Revision ID: 995e9d1b7ad2
Revises: 0cbcdecf840a
Create Date: 2018-10-07 00:01:36.794970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '995e9d1b7ad2'
down_revision = '0cbcdecf840a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instamentions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mention_username', sa.String(), nullable=True),
    sa.Column('comment_id', sa.String(), nullable=True),
    sa.Column('mention_timestamp', sa.String(), nullable=True),
    sa.Column('media_id', sa.String(), nullable=True),
    sa.Column('media_type', sa.String(), nullable=True),
    sa.Column('media_url', sa.String(), nullable=True),
    sa.Column('media_permalink', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instamentions_mention_username'), 'instamentions', ['mention_username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_instamentions_mention_username'), table_name='instamentions')
    op.drop_table('instamentions')
    # ### end Alembic commands ###
