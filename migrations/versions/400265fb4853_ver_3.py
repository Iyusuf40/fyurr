"""ver 3

Revision ID: 400265fb4853
Revises: 7587809294c9
Create Date: 2022-06-03 00:27:20.335135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '400265fb4853'
down_revision = '7587809294c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('website_link', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'website_link')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
