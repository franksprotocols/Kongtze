"""add_student_performance_analytics_table

Revision ID: 8579fb6bd3d6
Revises: a571152aaf34
Create Date: 2026-01-28 12:40:30.288171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8579fb6bd3d6'
down_revision: Union[str, None] = 'a571152aaf34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'student_performance_analytics',
        sa.Column('analytics_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('total_tests_taken', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('average_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('average_time_per_question', sa.Integer(), nullable=True),
        sa.Column('current_difficulty_level', sa.Integer(), nullable=True),
        sa.Column('recommended_difficulty_level', sa.Integer(), nullable=True),
        sa.Column('difficulty_trend', sa.String(length=20), nullable=True),
        sa.Column('period_start', sa.Date(), nullable=True),
        sa.Column('period_end', sa.Date(), nullable=True),
        sa.Column('difficulty_breakdown', sa.JSON(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('analytics_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], )
    )
    op.create_index(op.f('ix_student_performance_user_subject'), 'student_performance_analytics', ['user_id', 'subject_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_student_performance_user_subject'), table_name='student_performance_analytics')
    op.drop_table('student_performance_analytics')
