"""empty message

Revision ID: da55315d0028
Revises: 06a629b95cbc
Create Date: 2021-10-24 21:54:09.394392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da55315d0028'
down_revision = '06a629b95cbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar_image', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar_image')
    # ### end Alembic commands ###
