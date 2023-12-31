"""Optional projects

Revision ID: 07b2ff2691f6
Revises: 90c03f7e3449
Create Date: 2023-10-15 23:26:12.161980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b2ff2691f6'
down_revision = '90c03f7e3449'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('achievements', 'date',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('projects', 'idea',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('projects', 'status',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('projects', 'stage',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('projects', 'year',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('projects', 'division',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'division',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('projects', 'year',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('projects', 'stage',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('projects', 'status',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('projects', 'idea',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('achievements', 'date',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
