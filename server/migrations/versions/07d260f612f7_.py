"""empty message

Revision ID: 07d260f612f7
Revises: ea1ce1c043d6
Create Date: 2019-08-19 09:32:35.647283

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '07d260f612f7'
down_revision = 'ea1ce1c043d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mainproducts', sa.Column('is_fav', sa.Boolean(), nullable=True))
    op.add_column('mainproducts', sa.Column('searchable', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('looks', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'looks')
    op.drop_column('mainproducts', 'searchable')
    op.drop_column('mainproducts', 'is_fav')
    # ### end Alembic commands ###
