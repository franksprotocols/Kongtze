"""add_ai_prompt_templates_table

Revision ID: d22aa8e43ca2
Revises: 8579fb6bd3d6
Create Date: 2026-01-28 13:21:16.693614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd22aa8e43ca2'
down_revision: Union[str, None] = '8579fb6bd3d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ai_prompt_templates',
        sa.Column('template_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('template_name', sa.String(length=100), nullable=False),
        sa.Column('template_type', sa.String(length=50), nullable=False),
        sa.Column('prompt_template', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_system', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('template_id'),
        sa.UniqueConstraint('template_name')
    )
    op.create_index(op.f('ix_ai_prompt_templates_type'), 'ai_prompt_templates', ['template_type'], unique=False)
    op.create_index(op.f('ix_ai_prompt_templates_active'), 'ai_prompt_templates', ['is_active'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_ai_prompt_templates_active'), table_name='ai_prompt_templates')
    op.drop_index(op.f('ix_ai_prompt_templates_type'), table_name='ai_prompt_templates')
    op.drop_table('ai_prompt_templates')
