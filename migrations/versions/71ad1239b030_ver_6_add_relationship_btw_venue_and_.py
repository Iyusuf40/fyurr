"""ver 6 add relationship btw venue and par_venue, create par_venue

Revision ID: 71ad1239b030
Revises: d8df9b9e0f89
Create Date: 2022-06-03 10:21:02.955895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71ad1239b030'
down_revision = 'd8df9b9e0f89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Par_venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('venue', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['venue'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Par_venue')
    # ### end Alembic commands ###
