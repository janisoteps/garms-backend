"""empty message

Revision ID: a2436672d0d5
Revises: f4a3f38b7190
Create Date: 2018-05-27 01:14:58.321438

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a2436672d0d5'
down_revision = 'f4a3f38b7190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('color_3', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('color_3_hex', sa.String(), nullable=True))
    op.create_index(op.f('ix_products_brand'), 'products', ['brand'], unique=False)
    op.create_index(op.f('ix_products_color_name'), 'products', ['color_name'], unique=False)
    op.create_index(op.f('ix_products_img_cats_sc_txt'), 'products', ['img_cats_sc_txt'], unique=False)
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_index(op.f('ix_products_img_cats_sc_txt'), table_name='products')
    op.drop_index(op.f('ix_products_color_name'), table_name='products')
    op.drop_index(op.f('ix_products_brand'), table_name='products')
    op.drop_column('products', 'color_3_hex')
    op.drop_column('products', 'color_3')
    # ### end Alembic commands ###
