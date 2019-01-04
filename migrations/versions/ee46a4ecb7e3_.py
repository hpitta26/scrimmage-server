"""Add tournament status

Revision ID: ee46a4ecb7e3
Revises: 1ce0eb6f5f54
Create Date: 2019-01-03 18:59:43.630787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee46a4ecb7e3'
down_revision = '1ce0eb6f5f54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournaments', sa.Column('status', sa.Enum('created', 'spawned', 'spawning', name='tournamentstatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournaments', 'status')
    # ### end Alembic commands ###
