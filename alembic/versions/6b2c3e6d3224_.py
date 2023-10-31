"""empty message

Revision ID: 6b2c3e6d3224
Revises: 
Create Date: 2023-09-06 19:52:39.923577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b2c3e6d3224'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('patronym', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('user', 'organizer', 'admin', 'expert', name='userroles'), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('hobbies', sa.String(), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('social_networks', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('verified_email', sa.Boolean(), nullable=False),
    sa.Column('speciality', sa.String(), nullable=True),
    sa.Column('priority_direction', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('not_priority_direction', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('level', sa.String(), nullable=True),
    sa.Column('competencies', sa.String(), nullable=True),
    sa.Column('projects_to_show', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('is_expert', sa.Boolean(), nullable=True),
    sa.Column('users_allow_to_show_contacts', sa.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('education',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('education_start', sa.String(), nullable=False),
    sa.Column('education_end', sa.String(), nullable=False),
    sa.Column('diploma_img', sa.String(), nullable=True),
    sa.Column('education_type', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('idea', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('stage', sa.String(), nullable=False),
    sa.Column('achievements', sa.String(), nullable=False),
    sa.Column('year', sa.String(), nullable=False),
    sa.Column('division', sa.String(), nullable=False),
    sa.Column('images', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('file', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('team', sa.ARRAY(sa.JSON()), nullable=False),
    sa.Column('experts', sa.ARRAY(sa.JSON()), nullable=True),
    sa.Column('description_fullness', sa.Integer(), nullable=False),
    sa.Column('is_published', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_invited',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'project_id')
    )
    op.create_table('user_responded',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'project_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_responded')
    op.drop_table('user_invited')
    op.drop_table('projects')
    op.drop_table('education')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
