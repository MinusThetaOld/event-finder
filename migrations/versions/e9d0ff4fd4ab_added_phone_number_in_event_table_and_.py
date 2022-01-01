"""added phone number in event table and deleted phone number from profile

Revision ID: e9d0ff4fd4ab
Revises: bac87e1894d3
Create Date: 2022-01-01 20:35:01.263044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9d0ff4fd4ab'
down_revision = 'bac87e1894d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('phone_number', sa.String(), nullable=True))
    op.drop_column('profile', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('event', 'phone_number')
    # ### end Alembic commands ###
