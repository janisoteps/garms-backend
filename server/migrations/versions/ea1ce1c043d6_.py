"""empty message

Revision ID: ea1ce1c043d6
Revises: 56b39cda71b0
Create Date: 2019-08-15 00:55:28.792448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ea1ce1c043d6'
down_revision = '56b39cda71b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('wardrobe', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'wardrobe')
    # ### end Alembic commands ###