"""empty message

Revision ID: acbb795d547f
Revises: a7d85639127f
Create Date: 2020-04-06 17:58:17.307392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acbb795d547f'
down_revision = 'a7d85639127f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prods_men_a', sa.Column('name', sa.Text(), nullable=True))
    op.create_index(op.f('ix_prods_men_a_name'), 'prods_men_a', ['name'], unique=False)
    op.drop_index('ix_prods_men_a_prod_name_men', table_name='prods_men_a')
    op.drop_index('prods_men_a_name_idx', table_name='prods_men_a')
    op.drop_column('prods_men_a', 'prod_name_men')
    op.add_column('prods_women_a', sa.Column('name', sa.Text(), nullable=True))
    op.create_index(op.f('ix_prods_women_a_name'), 'prods_women_a', ['name'], unique=False)
    op.drop_index('ix_prods_women_a_prod_name_women', table_name='prods_women_a')
    op.drop_index('prods_women_a_name_idx', table_name='prods_women_a')
    op.drop_column('prods_women_a', 'prod_name_women')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prods_women_a', sa.Column('prod_name_women', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('prods_women_a_name_idx', 'prods_women_a', ['prod_name_women'], unique=False)
    op.create_index('ix_prods_women_a_prod_name_women', 'prods_women_a', ['prod_name_women'], unique=False)
    op.drop_index(op.f('ix_prods_women_a_name'), table_name='prods_women_a')
    op.drop_column('prods_women_a', 'name')
    op.add_column('prods_men_a', sa.Column('prod_name_men', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('prods_men_a_name_idx', 'prods_men_a', ['prod_name_men'], unique=False)
    op.create_index('ix_prods_men_a_prod_name_men', 'prods_men_a', ['prod_name_men'], unique=False)
    op.drop_index(op.f('ix_prods_men_a_name'), table_name='prods_men_a')
    op.drop_column('prods_men_a', 'name')
    # ### end Alembic commands ###
