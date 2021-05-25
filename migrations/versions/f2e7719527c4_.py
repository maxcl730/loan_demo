"""empty message

Revision ID: f2e7719527c4
Revises: a47ca0b5271b
Create Date: 2021-05-19 12:02:36.717936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2e7719527c4'
down_revision = 'a47ca0b5271b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'address', 'member', ['member_id'], ['id'])
    op.create_foreign_key(None, 'application', 'member', ['member_id'], ['id'])
    op.create_foreign_key(None, 'debit', 'member', ['member_id'], ['id'])
    op.create_foreign_key(None, 'roles_users', 'role', ['role_id'], ['id'])
    op.create_foreign_key(None, 'roles_users', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles_users', type_='foreignkey')
    op.drop_constraint(None, 'roles_users', type_='foreignkey')
    op.drop_constraint(None, 'debit', type_='foreignkey')
    op.drop_constraint(None, 'application', type_='foreignkey')
    op.drop_constraint(None, 'address', type_='foreignkey')
    # ### end Alembic commands ###
