"""
Revision ID: 20250101_01_initial_billing_tables
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250101_01_initial_billing_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create subscription_plan table
    op.create_table('subscription_plan',
        sa.Column('plan_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('limits', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('price_per_month', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('plan_id')
    )

    # Create tenant_billing_profile table
    op.create_table('tenant_billing_profile',
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('plan_id', sa.String(), nullable=True),
        sa.Column('billing_email', sa.String(), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('trial_expiry', sa.DateTime(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('tenant_id')
    )

    # Create billing_event table
    op.create_table('billing_event',
        sa.Column('event_id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('event_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('event_id')
    )

def downgrade():
    op.drop_table('billing_event')
    op.drop_table('tenant_billing_profile')
    op.drop_table('subscription_plan') 