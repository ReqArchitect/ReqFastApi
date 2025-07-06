"""
Revision ID: 20250101_01_initial_ai_modeling_tables
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250101_01_initial_ai_modeling_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create modeling_input table
    op.create_table('modeling_input',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('input_type', sa.String(), nullable=True),
        sa.Column('input_text', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_modeling_input_tenant_id'), 'modeling_input', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_modeling_input_user_id'), 'modeling_input', ['user_id'], unique=False)

    # Create modeling_output table
    op.create_table('modeling_output',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('input_id', sa.Integer(), nullable=True),
        sa.Column('layer', sa.String(), nullable=True),
        sa.Column('elements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('traceability', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create modeling_feedback table
    op.create_table('modeling_feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('output_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('comments', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('modeling_feedback')
    op.drop_table('modeling_output')
    op.drop_index(op.f('ix_modeling_input_user_id'), table_name='modeling_input')
    op.drop_index(op.f('ix_modeling_input_tenant_id'), table_name='modeling_input')
    op.drop_table('modeling_input') 