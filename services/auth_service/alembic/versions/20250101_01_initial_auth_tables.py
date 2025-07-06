"""
Revision ID: 20250101_01_initial_auth_tables
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250101_01_initial_auth_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create user table
    op.create_table('user',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_tenant_id'), 'user', ['tenant_id'], unique=False)

    # Create auth_token table
    op.create_table('auth_token',
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('issued_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('token')
    )
    op.create_index(op.f('ix_auth_token_user_id'), 'auth_token', ['user_id'], unique=False)
    op.create_index(op.f('ix_auth_token_tenant_id'), 'auth_token', ['tenant_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_auth_token_tenant_id'), table_name='auth_token')
    op.drop_index(op.f('ix_auth_token_user_id'), table_name='auth_token')
    op.drop_table('auth_token')
    op.drop_index(op.f('ix_user_tenant_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user') 