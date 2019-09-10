"""empty message

Revision ID: 3fb88b83e043
Revises: 07d260f612f7
Create Date: 2019-09-10 12:02:00.378249

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3fb88b83e043'
down_revision = '07d260f612f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_hash', sa.String(length=40), nullable=True),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('prod_id', sa.String(), nullable=True),
    sa.Column('prod_url', sa.String(), nullable=True),
    sa.Column('color_string', sa.String(), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sale', sa.Boolean(), nullable=True),
    sa.Column('saleprice', sa.Float(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('shop', sa.String(), nullable=True),
    sa.Column('kind_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('color_pattern_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('style_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('material_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('attribute_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('filter_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('all_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('kind_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('col_pat_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('style_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('material_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('attr_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('filter_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('all_arr', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_1', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_1_hex', sa.String(), nullable=True),
    sa.Column('color_2', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_2_hex', sa.String(), nullable=True),
    sa.Column('color_3', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_3_hex', sa.String(), nullable=True),
    sa.Column('encoding_crop', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('size_stock', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_v2_color_string'), 'images_v2', ['color_string'], unique=False)
    op.create_index(op.f('ix_images_v2_img_hash'), 'images_v2', ['img_hash'], unique=True)
    op.create_index(op.f('ix_images_v2_kind_cats'), 'images_v2', ['kind_cats'], unique=False)
    op.create_index(op.f('ix_images_v2_name'), 'images_v2', ['name'], unique=False)
    op.create_index('name_idx', 'images_v2', ['name'], unique=False, postgresql_ops={'name': 'gin_trgm_ops'}, postgresql_using='gin')
    op.add_column('products', sa.Column('all_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('all_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('attr_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('attribute_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('category', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('col_pat_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('color_pattern_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('color_string', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('filter_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('filter_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('image_hash', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('image_urls', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('kind_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('kind_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('material_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('material_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('products', sa.Column('prod_id', sa.String(length=40), nullable=True))
    op.add_column('products', sa.Column('size_stock', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('products', sa.Column('style_arr', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column('products', sa.Column('style_cats', postgresql.ARRAY(sa.String()), nullable=True))
    op.create_index(op.f('ix_products_image_hash'), 'products', ['image_hash'], unique=False)
    op.create_index(op.f('ix_products_kind_cats'), 'products', ['kind_cats'], unique=False)
    op.create_index(op.f('ix_products_prod_id'), 'products', ['prod_id'], unique=True)
    op.drop_index('ix_products_brand', table_name='products')
    op.drop_index('ix_products_color_name', table_name='products')
    op.drop_index('ix_products_img_cats_ai_txt', table_name='products')
    op.drop_index('ix_products_img_cats_sc_txt', table_name='products')
    op.drop_index('ix_products_img_hash', table_name='products')
    op.drop_index('ix_products_name', table_name='products')
    op.drop_index('ix_products_spider_cat', table_name='products')
    op.drop_column('products', 'color_2')
    op.drop_column('products', 'img_cats_sc_txt')
    op.drop_column('products', 'color_2_hex')
    op.drop_column('products', 'spider_cat')
    op.drop_column('products', 'color_1_hex')
    op.drop_column('products', 'pattern_256')
    op.drop_column('products', 'pca_256')
    op.drop_column('products', 'img_hash')
    op.drop_column('products', 'img_cats_ai_txt')
    op.drop_column('products', 'siamese_64')
    op.drop_column('products', 'color_512')
    op.drop_column('products', 'color_1')
    op.drop_column('products', 'color_3_hex')
    op.drop_column('products', 'img_url')
    op.drop_column('products', 'img_urls')
    op.drop_column('products', 'color_name')
    op.drop_column('products', 'color_3')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('color_3', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('img_urls', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('img_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_3_hex', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_1', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_512', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('siamese_64', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('img_cats_ai_txt', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('img_hash', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('pca_256', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('pattern_256', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_1_hex', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('spider_cat', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_2_hex', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('img_cats_sc_txt', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('color_2', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.create_index('ix_products_spider_cat', 'products', ['spider_cat'], unique=False)
    op.create_index('ix_products_name', 'products', ['name'], unique=False)
    op.create_index('ix_products_img_hash', 'products', ['img_hash'], unique=True)
    op.create_index('ix_products_img_cats_sc_txt', 'products', ['img_cats_sc_txt'], unique=False)
    op.create_index('ix_products_img_cats_ai_txt', 'products', ['img_cats_ai_txt'], unique=False)
    op.create_index('ix_products_color_name', 'products', ['color_name'], unique=False)
    op.create_index('ix_products_brand', 'products', ['brand'], unique=False)
    op.drop_index(op.f('ix_products_prod_id'), table_name='products')
    op.drop_index(op.f('ix_products_kind_cats'), table_name='products')
    op.drop_index(op.f('ix_products_image_hash'), table_name='products')
    op.drop_column('products', 'style_cats')
    op.drop_column('products', 'style_arr')
    op.drop_column('products', 'size_stock')
    op.drop_column('products', 'prod_id')
    op.drop_column('products', 'material_cats')
    op.drop_column('products', 'material_arr')
    op.drop_column('products', 'kind_cats')
    op.drop_column('products', 'kind_arr')
    op.drop_column('products', 'image_urls')
    op.drop_column('products', 'image_hash')
    op.drop_column('products', 'filter_cats')
    op.drop_column('products', 'filter_arr')
    op.drop_column('products', 'color_string')
    op.drop_column('products', 'color_pattern_cats')
    op.drop_column('products', 'col_pat_arr')
    op.drop_column('products', 'category')
    op.drop_column('products', 'attribute_cats')
    op.drop_column('products', 'attr_arr')
    op.drop_column('products', 'all_cats')
    op.drop_column('products', 'all_arr')
    op.drop_index('name_idx', table_name='images_v2')
    op.drop_index(op.f('ix_images_v2_name'), table_name='images_v2')
    op.drop_index(op.f('ix_images_v2_kind_cats'), table_name='images_v2')
    op.drop_index(op.f('ix_images_v2_img_hash'), table_name='images_v2')
    op.drop_index(op.f('ix_images_v2_color_string'), table_name='images_v2')
    op.drop_table('images_v2')
    # ### end Alembic commands ###
