"""
Revision ID: 20250101_01_initial_invoice_tables
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250101_01_initial_invoice_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create invoices table
    op.create_table('invoices',
        sa.Column('invoice_id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('billing_period_start', sa.DateTime(), nullable=False),
        sa.Column('billing_period_end', sa.DateTime(), nullable=False),
        sa.Column('line_items', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('pdf_url', sa.String(), nullable=True),
        sa.Column('stripe_invoice_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('invoice_id')
    )

def downgrade():
    op.drop_table('invoices') 