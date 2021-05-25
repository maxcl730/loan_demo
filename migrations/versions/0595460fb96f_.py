"""empty message

Revision ID: 0595460fb96f
Revises: f2e7719527c4
Create Date: 2021-05-19 12:03:38.226956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0595460fb96f'
down_revision = 'f2e7719527c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'address', 'member', ['member_id'], ['id'])
    op.create_foreign_key(None, 'application', 'member', ['member_id'], ['id'])
    op.create_foreign_key(None, 'debit', 'member', ['member_id'], ['id'])
    op.create_foreign_key(None, 'roles_users', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'roles_users', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles_users', type_='foreignkey')
    op.drop_constraint(None, 'roles_users', type_='foreignkey')
    op.drop_constraint(None, 'debit', type_='foreignkey')
    op.drop_constraint(None, 'application', type_='foreignkey')
    op.drop_constraint(None, 'address', type_='foreignkey')
    # ### end Alembic commands ###
