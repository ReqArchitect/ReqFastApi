"""
Revision ID: 20250101_01_initial_notification_tables
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250101_01_initial_notification_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create notification table
    op.create_table('notification',
        sa.Column('notification_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('channel', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=True),
        sa.Column('delivered', sa.Boolean(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_index(op.f('ix_notification_user_id'), 'notification', ['user_id'], unique=False)
    op.create_index(op.f('ix_notification_tenant_id'), 'notification', ['tenant_id'], unique=False)

    # Create notification_template table
    op.create_table('notification_template',
        sa.Column('template_id', sa.String(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=True),
        sa.Column('channel', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('template_id')
    )
    op.create_index(op.f('ix_notification_template_event_type'), 'notification_template', ['event_type'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_notification_template_event_type'), table_name='notification_template')
    op.drop_table('notification_template')
    op.drop_index(op.f('ix_notification_tenant_id'), table_name='notification')
    op.drop_index(op.f('ix_notification_user_id'), table_name='notification')
    op.drop_table('notification') 