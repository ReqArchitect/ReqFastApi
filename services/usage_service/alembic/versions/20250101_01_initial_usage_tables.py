"""
Revision ID: 20250101_01_initial_usage_tables
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250101_01_initial_usage_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create usage_metrics table
    op.create_table('usage_metrics',
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('active_users', sa.Integer(), nullable=True),
        sa.Column('model_count', sa.Integer(), nullable=True),
        sa.Column('api_requests', sa.Integer(), nullable=True),
        sa.Column('data_footprint', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('tenant_id')
    )

    # Create audit_events table
    op.create_table('audit_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=True),
        sa.Column('event_time', sa.DateTime(), nullable=True),
        sa.Column('details', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_events_tenant_id'), 'audit_events', ['tenant_id'], unique=False)

    # Create system_stats table
    op.create_table('system_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uptime_percent', sa.Float(), nullable=True),
        sa.Column('error_rate_percent', sa.Float(), nullable=True),
        sa.Column('p95_latency_ms', sa.Float(), nullable=True),
        sa.Column('collected_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('system_stats')
    op.drop_index(op.f('ix_audit_events_tenant_id'), table_name='audit_events')
    op.drop_table('audit_events')
    op.drop_table('usage_metrics') 