"""Caching of user avatar hashes (10d)

Revision ID: 79be831df19d
Revises: a4f00c43a719
Create Date: 2019-12-20 18:57:19.715267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79be831df19d'
down_revision = 'a4f00c43a719'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###