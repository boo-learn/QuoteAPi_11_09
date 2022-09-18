"""add User

Revision ID: 428fdf7778d5
Revises: 050d1b570187
Create Date: 2022-09-18 04:29:30.043237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '428fdf7778d5'
down_revision = '050d1b570187'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_model_username'), 'user_model', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_model_username'), table_name='user_model')
    op.drop_table('user_model')
    # ### end Alembic commands ###