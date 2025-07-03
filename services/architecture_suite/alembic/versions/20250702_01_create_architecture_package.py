"""
Revision ID: 20250702_01
Revises: 
Create Date: 2025-07-02
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'business_case',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id'), nullable=False),
    )
    op.create_table(
        'initiative',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id'), nullable=False),
    )
    op.create_table(
        'kpi_service',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id'), nullable=False),
    )
    op.create_table(
        'business_model_canvas',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id'), nullable=False),
    )
    op.create_table(
        'architecture_package',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant.id'), nullable=False),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('business_case_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('business_case.id'), nullable=False),
        sa.Column('initiative_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('initiative.id'), nullable=False),
        sa.Column('kpi_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('kpi_service.id'), nullable=False),
        sa.Column('business_model_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('business_model_canvas.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'architecture_element_link',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('package_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('architecture_package.id'), nullable=False),
        sa.Column('element_type', sa.String(), nullable=False),
        sa.Column('element_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('traceability_fk', sa.String(), nullable=False),
    )

def downgrade():
    op.drop_table('architecture_package')
