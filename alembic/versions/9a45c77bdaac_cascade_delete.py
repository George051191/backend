"""cascade delete

Revision ID: 9a45c77bdaac
Revises: 2eba475f416b
Create Date: 2023-10-20 17:16:04.077549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a45c77bdaac'
down_revision = '2eba475f416b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('achievements_folder_id_fkey', 'achievements', type_='foreignkey')
    op.drop_constraint('achievements_owner_id_fkey', 'achievements', type_='foreignkey')
    op.create_foreign_key(None, 'achievements', 'achievement_folder', ['folder_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'achievements', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'achievements', type_='foreignkey')
    op.drop_constraint(None, 'achievements', type_='foreignkey')
    op.create_foreign_key('achievements_owner_id_fkey', 'achievements', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('achievements_folder_id_fkey', 'achievements', 'achievement_folder', ['folder_id'], ['id'])
    # ### end Alembic commands ###