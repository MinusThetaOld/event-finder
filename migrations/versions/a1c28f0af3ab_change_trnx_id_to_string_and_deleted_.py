"""change trnx id to string and deleted pending members column

Revision ID: a1c28f0af3ab
Revises: 0e2baa96ac68
Create Date: 2022-01-01 19:36:18.016562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1c28f0af3ab'
down_revision = '0e2baa96ac68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'pending_members')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('pending_members', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###