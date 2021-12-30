"""Created is open column in Event table

Revision ID: 0e2baa96ac68
Revises: c0e800c86f3c
Create Date: 2021-12-30 18:47:01.352791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e2baa96ac68'
down_revision = 'c0e800c86f3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('is_open', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'is_open')
    # ### end Alembic commands ###
