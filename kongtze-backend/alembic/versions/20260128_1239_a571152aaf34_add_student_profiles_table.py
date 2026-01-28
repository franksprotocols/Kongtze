"""add_student_profiles_table

Revision ID: a571152aaf34
Revises: f4e4da42c823
Create Date: 2026-01-28 12:39:32.406055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a571152aaf34'
down_revision: Union[str, None] = 'f4e4da42c823'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'student_profiles',
        sa.Column('profile_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('grade_level', sa.String(length=50), nullable=True),
        sa.Column('school_name', sa.String(length=255), nullable=True),
        sa.Column('math_level', sa.String(length=50), nullable=True),
        sa.Column('english_level', sa.String(length=50), nullable=True),
        sa.Column('chinese_level', sa.String(length=50), nullable=True),
        sa.Column('strengths', sa.JSON(), nullable=True),
        sa.Column('weaknesses', sa.JSON(), nullable=True),
        sa.Column('learning_pace', sa.String(length=50), nullable=True),
        sa.Column('preferred_question_types', sa.JSON(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('profile_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_student_profiles_user_id'), 'student_profiles', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_student_profiles_user_id'), table_name='student_profiles')
    op.drop_table('student_profiles')
