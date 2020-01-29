"""empty message

Revision ID: 56ff3d75986e
Revises: 2edd547ec807
Create Date: 2020-01-29 14:47:02.918151

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '56ff3d75986e'
down_revision = '2edd547ec807'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images_full_women_a',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_hash', sa.String(length=40), nullable=True),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('prod_id', sa.String(), nullable=True),
    sa.Column('prod_url', sa.String(), nullable=True),
    sa.Column('brand', sa.Text(), nullable=True),
    sa.Column('color_string', sa.String(), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('img_full_name', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sale', sa.Boolean(), nullable=True),
    sa.Column('saleprice', sa.Float(), nullable=True),
    sa.Column('discount_rate', sa.Float(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('shop', sa.String(), nullable=True),
    sa.Column('kind_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('pattern_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('color_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('style_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('material_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('attribute_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('length_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('filter_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('all_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('color_1', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_1_hex', sa.String(), nullable=True),
    sa.Column('color_2', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_2_hex', sa.String(), nullable=True),
    sa.Column('color_3', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_3_hex', sa.String(), nullable=True),
    sa.Column('size_stock', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.Column('encoding_vgg16', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('images_full_women_a_name_idx', 'images_full_women_a', ['img_full_name'], unique=False, postgresql_ops={'img_full_name': 'gin_trgm_ops'}, postgresql_using='gin')
    op.create_index(op.f('ix_images_full_women_a_all_cats'), 'images_full_women_a', ['all_cats'], unique=False)
    op.create_index(op.f('ix_images_full_women_a_img_full_name'), 'images_full_women_a', ['img_full_name'], unique=False)
    op.create_index(op.f('ix_images_full_women_a_img_hash'), 'images_full_women_a', ['img_hash'], unique=True)
    op.create_index(op.f('ix_images_full_women_a_kind_cats'), 'images_full_women_a', ['kind_cats'], unique=False)
    op.create_table('images_skinny_women_a',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('img_hash', sa.String(length=40), nullable=False),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('prod_id', sa.String(), nullable=True),
    sa.Column('prod_url', sa.String(), nullable=True),
    sa.Column('brand', sa.Text(), nullable=True),
    sa.Column('color_string', sa.String(), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('img_skinny_name', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sale', sa.Boolean(), nullable=True),
    sa.Column('saleprice', sa.Float(), nullable=True),
    sa.Column('discount_rate', sa.Float(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('shop', sa.String(), nullable=True),
    sa.Column('kind_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('pattern_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('color_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('style_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('material_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('attribute_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('length_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('filter_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('all_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('size_stock', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.Column('color_1', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_2', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('color_3', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('img_hash')
    )
    op.create_index('images_skinny_women_a_name_idx', 'images_skinny_women_a', ['img_skinny_name'], unique=False, postgresql_ops={'img_skinny_name': 'gin_trgm_ops'}, postgresql_using='gin')
    op.create_index(op.f('ix_images_skinny_women_a_all_cats'), 'images_skinny_women_a', ['all_cats'], unique=False)
    op.create_index(op.f('ix_images_skinny_women_a_img_hash'), 'images_skinny_women_a', ['img_hash'], unique=True)
    op.create_index(op.f('ix_images_skinny_women_a_img_skinny_name'), 'images_skinny_women_a', ['img_skinny_name'], unique=False)
    op.create_index(op.f('ix_images_skinny_women_a_kind_cats'), 'images_skinny_women_a', ['kind_cats'], unique=False)
    op.create_table('prods_women_a',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prod_id', sa.String(length=40), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('prod_url', sa.String(), nullable=True),
    sa.Column('brand', sa.Text(), nullable=True),
    sa.Column('category', sa.Text(), nullable=True),
    sa.Column('color_string', sa.Text(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image_hash', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('image_urls', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sale', sa.Boolean(), nullable=True),
    sa.Column('saleprice', sa.Float(), nullable=True),
    sa.Column('discount_rate', sa.Float(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('shop', sa.Text(), nullable=True),
    sa.Column('kind_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('pattern_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('color_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('style_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('material_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('attribute_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('length_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('filter_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('all_cats', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('size_stock', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.Column('is_fav', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prods_women_a_image_hash'), 'prods_women_a', ['image_hash'], unique=False)
    op.create_index(op.f('ix_prods_women_a_kind_cats'), 'prods_women_a', ['kind_cats'], unique=False)
    op.create_index(op.f('ix_prods_women_a_name'), 'prods_women_a', ['name'], unique=False)
    op.create_index(op.f('ix_prods_women_a_prod_id'), 'prods_women_a', ['prod_id'], unique=True)
    op.drop_index('ix_mainproducts_brand', table_name='mainproducts')
    op.drop_index('ix_mainproducts_img_cats_sc_txt', table_name='mainproducts')
    op.drop_index('ix_mainproducts_img_hashes', table_name='mainproducts')
    op.drop_index('ix_mainproducts_name', table_name='mainproducts')
    op.drop_index('ix_mainproducts_prod_hash', table_name='mainproducts')
    op.drop_index('ix_mainproducts_spider_cat', table_name='mainproducts')
    op.drop_table('mainproducts')
    op.drop_index('ix_images_brand', table_name='images')
    op.drop_index('ix_images_color_name', table_name='images')
    op.drop_index('ix_images_img_cats_ai_txt', table_name='images')
    op.drop_index('ix_images_img_cats_sc_txt', table_name='images')
    op.drop_index('ix_images_img_hash', table_name='images')
    op.drop_index('ix_images_name', table_name='images')
    op.drop_index('ix_images_spider_cat', table_name='images')
    op.drop_index('name_idx', table_name='images')
    op.drop_table('images')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('img_hash', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('prod_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('img_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('brand', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('shop', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('sale', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('saleprice', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('spider_cat', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('img_cats_ai_txt', postgresql.ARRAY(sa.TEXT()), autoincrement=False, nullable=True),
    sa.Column('img_cats_sc_txt', postgresql.ARRAY(sa.TEXT()), autoincrement=False, nullable=True),
    sa.Column('color_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('color_512', postgresql.ARRAY(postgresql.DOUBLE_PRECISION(precision=53)), autoincrement=False, nullable=True),
    sa.Column('color_1', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('color_1_hex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('color_2', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('color_2_hex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('color_3', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('color_3_hex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('encoding_nocrop', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('encoding_crop', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('encoding_squarecrop', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='images_pkey')
    )
    op.create_index('name_idx', 'images', ['name'], unique=False)
    op.create_index('ix_images_spider_cat', 'images', ['spider_cat'], unique=False)
    op.create_index('ix_images_name', 'images', ['name'], unique=False)
    op.create_index('ix_images_img_hash', 'images', ['img_hash'], unique=True)
    op.create_index('ix_images_img_cats_sc_txt', 'images', ['img_cats_sc_txt'], unique=False)
    op.create_index('ix_images_img_cats_ai_txt', 'images', ['img_cats_ai_txt'], unique=False)
    op.create_index('ix_images_color_name', 'images', ['color_name'], unique=False)
    op.create_index('ix_images_brand', 'images', ['brand'], unique=False)
    op.create_table('mainproducts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('prod_hash', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('prod_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('brand', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('shop', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('sale', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('saleprice', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('img_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('img_urls', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('img_hashes', postgresql.ARRAY(sa.VARCHAR(length=40)), autoincrement=False, nullable=True),
    sa.Column('spider_cat', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('img_cats_sc_txt', postgresql.ARRAY(sa.TEXT()), autoincrement=False, nullable=True),
    sa.Column('is_fav', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('searchable', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='mainproducts_pkey')
    )
    op.create_index('ix_mainproducts_spider_cat', 'mainproducts', ['spider_cat'], unique=False)
    op.create_index('ix_mainproducts_prod_hash', 'mainproducts', ['prod_hash'], unique=True)
    op.create_index('ix_mainproducts_name', 'mainproducts', ['name'], unique=False)
    op.create_index('ix_mainproducts_img_hashes', 'mainproducts', ['img_hashes'], unique=False)
    op.create_index('ix_mainproducts_img_cats_sc_txt', 'mainproducts', ['img_cats_sc_txt'], unique=False)
    op.create_index('ix_mainproducts_brand', 'mainproducts', ['brand'], unique=False)
    op.drop_index(op.f('ix_prods_women_a_prod_id'), table_name='prods_women_a')
    op.drop_index(op.f('ix_prods_women_a_name'), table_name='prods_women_a')
    op.drop_index(op.f('ix_prods_women_a_kind_cats'), table_name='prods_women_a')
    op.drop_index(op.f('ix_prods_women_a_image_hash'), table_name='prods_women_a')
    op.drop_table('prods_women_a')
    op.drop_index(op.f('ix_images_skinny_women_a_kind_cats'), table_name='images_skinny_women_a')
    op.drop_index(op.f('ix_images_skinny_women_a_img_skinny_name'), table_name='images_skinny_women_a')
    op.drop_index(op.f('ix_images_skinny_women_a_img_hash'), table_name='images_skinny_women_a')
    op.drop_index(op.f('ix_images_skinny_women_a_all_cats'), table_name='images_skinny_women_a')
    op.drop_index('images_skinny_women_a_name_idx', table_name='images_skinny_women_a')
    op.drop_table('images_skinny_women_a')
    op.drop_index(op.f('ix_images_full_women_a_kind_cats'), table_name='images_full_women_a')
    op.drop_index(op.f('ix_images_full_women_a_img_hash'), table_name='images_full_women_a')
    op.drop_index(op.f('ix_images_full_women_a_img_full_name'), table_name='images_full_women_a')
    op.drop_index(op.f('ix_images_full_women_a_all_cats'), table_name='images_full_women_a')
    op.drop_index('images_full_women_a_name_idx', table_name='images_full_women_a')
    op.drop_table('images_full_women_a')
    # ### end Alembic commands ###
