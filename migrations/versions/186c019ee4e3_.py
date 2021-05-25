"""empty message

Revision ID: 186c019ee4e3
Revises: 0595460fb96f
Create Date: 2021-05-20 12:08:50.255445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186c019ee4e3'
down_revision = '0595460fb96f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repayment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('paid_status', sa.Integer(), nullable=False),
    sa.Column('term', sa.Integer(), nullable=False),
    sa.Column('payment_due_date', sa.DateTime(), nullable=False),
    sa.Column('fee', sa.Float(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('application_id', 'term', name='uix_application_term')
    )
    op.create_index(op.f('ix_repayment_application_id'), 'repayment', ['application_id'], unique=False)
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
    op.drop_index(op.f('ix_repayment_application_id'), table_name='repayment')
    op.drop_table('repayment')
    # ### end Alembic commands ###
