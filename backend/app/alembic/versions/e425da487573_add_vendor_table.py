"""add vendor table

Revision ID: e425da487573
Revises: 1a31ce608336
Create Date: 2024-08-06 15:44:37.798648

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'e425da487573'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vendor',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('vendor_code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vendor')
    # ### end Alembic commands ###
