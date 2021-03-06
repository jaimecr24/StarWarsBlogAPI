"""empty message

Revision ID: b901b85a9331
Revises: 9fd6c98b617f
Create Date: 2021-11-10 20:51:25.449086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b901b85a9331'
down_revision = '9fd6c98b617f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('terrain', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planet')
    # ### end Alembic commands ###
