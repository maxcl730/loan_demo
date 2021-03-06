"""empty message

Revision ID: f13b4605ab6c
Revises: 
Create Date: 2021-05-25 20:17:47.455297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f13b4605ab6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('national_id', sa.String(length=20), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=False),
    sa.Column('birthday', sa.String(length=20), nullable=True),
    sa.Column('mobile', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('salt', sa.String(length=32), nullable=True),
    sa.Column('reg_ip', sa.String(length=20), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('blocked_info', sa.Text(), nullable=True),
    sa.Column('language', sa.String(length=20), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_member_mobile'), 'member', ['mobile'], unique=False)
    op.create_index(op.f('ix_member_national_id'), 'member', ['national_id'], unique=False)
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=100), nullable=True),
    sa.Column('current_login_ip', sa.String(length=100), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('fs_uniquifier', sa.String(length=255), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('postal_code', sa.String(length=20), nullable=False),
    sa.Column('province_name', sa.String(length=50), nullable=False),
    sa.Column('city_name', sa.String(length=50), nullable=False),
    sa.Column('county_name', sa.String(length=50), nullable=False),
    sa.Column('detail_info', sa.String(length=200), nullable=False),
    sa.Column('national_code', sa.String(length=20), nullable=False),
    sa.Column('tel_number', sa.String(length=30), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('term', sa.Integer(), nullable=False),
    sa.Column('apr', sa.Float(), nullable=False),
    sa.Column('method', sa.String(length=1), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_application_member_id'), 'application', ['member_id'], unique=False)
    op.create_table('debit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), autoincrement=True, nullable=False),
    sa.Column('number', sa.String(length=50), autoincrement=True, nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('member_id')
    )
    op.create_index(op.f('ix_debit_number'), 'debit', ['number'], unique=False)
    op.create_table('roles_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('repayment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('paid_status', sa.Integer(), nullable=False),
    sa.Column('sequence', sa.Integer(), nullable=False),
    sa.Column('payment_due_date', sa.DateTime(), nullable=False),
    sa.Column('fee', sa.Float(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('application_id', 'sequence', name='uix_application_sequence')
    )
    op.create_index(op.f('ix_repayment_application_id'), 'repayment', ['application_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_repayment_application_id'), table_name='repayment')
    op.drop_table('repayment')
    op.drop_table('roles_users')
    op.drop_index(op.f('ix_debit_number'), table_name='debit')
    op.drop_table('debit')
    op.drop_index(op.f('ix_application_member_id'), table_name='application')
    op.drop_table('application')
    op.drop_table('address')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_index(op.f('ix_member_national_id'), table_name='member')
    op.drop_index(op.f('ix_member_mobile'), table_name='member')
    op.drop_table('member')
    # ### end Alembic commands ###
