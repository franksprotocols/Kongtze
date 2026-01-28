"""Initial schema with all 12 tables

Revision ID: db5b77c9235b
Revises: 
Create Date: 2026-01-21 13:07:14.858466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db5b77c9235b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('pin', sa.String(length=4), nullable=True),
        sa.Column('is_parent', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create subjects table
    op.create_table(
        'subjects',
        sa.Column('subject_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('subject_id'),
        sa.UniqueConstraint('name')
    )

    # Create study_sessions table
    op.create_table(
        'study_sessions',
        sa.Column('session_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], ),
        sa.PrimaryKeyConstraint('session_id')
    )

    # Create tests table
    op.create_table(
        'tests',
        sa.Column('test_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('difficulty_level', sa.Integer(), nullable=False),
        sa.Column('time_limit_minutes', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('total_questions', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], ),
        sa.PrimaryKeyConstraint('test_id')
    )

    # Create questions table
    op.create_table(
        'questions',
        sa.Column('question_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('correct_answer', sa.String(length=1), nullable=False),
        sa.Column('time_limit_seconds', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_id'], ['tests.test_id'], ),
        sa.PrimaryKeyConstraint('question_id')
    )

    # Create test_results table
    op.create_table(
        'test_results',
        sa.Column('result_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('total_score', sa.Integer(), nullable=False),
        sa.Column('time_taken_seconds', sa.Integer(), nullable=False),
        sa.Column('answers', sa.JSON(), nullable=False),
        sa.Column('reward_points', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_id'], ['tests.test_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('result_id')
    )

    # Create homework table
    op.create_table(
        'homework',
        sa.Column('homework_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('photo_path', sa.String(length=500), nullable=False),
        sa.Column('ocr_text', sa.Text(), nullable=True),
        sa.Column('parent_reviewed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], ),
        sa.PrimaryKeyConstraint('homework_id')
    )

    # Create class_notes table
    op.create_table(
        'class_notes',
        sa.Column('note_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('photo_path', sa.String(length=500), nullable=False),
        sa.Column('ocr_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], ),
        sa.PrimaryKeyConstraint('note_id')
    )

    # Create topics table
    op.create_table(
        'topics',
        sa.Column('topic_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('note_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('topic_name', sa.String(length=255), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('extracted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['note_id'], ['class_notes.note_id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], ),
        sa.PrimaryKeyConstraint('topic_id')
    )

    # Create rewards table
    op.create_table(
        'rewards',
        sa.Column('reward_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=False),
        sa.Column('balance', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('reward_id')
    )

    # Create gifts table
    op.create_table(
        'gifts',
        sa.Column('gift_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('tier', sa.String(length=20), nullable=False),
        sa.Column('probability', sa.Float(), nullable=False),
        sa.Column('image_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('gift_id')
    )

    # Create cached_explanations table
    op.create_table(
        'cached_explanations',
        sa.Column('question_hash', sa.String(length=64), nullable=False),
        sa.Column('ai_explanation', sa.Text(), nullable=False),
        sa.Column('hit_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_accessed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('question_hash')
    )

    # Seed subjects data
    op.execute("""
        INSERT INTO subjects (name, display_name, description) VALUES
        ('math', 'Mathematics', 'Mathematical subjects including arithmetic, algebra, and geometry'),
        ('english', 'English', 'English language learning and literature'),
        ('chinese', 'Chinese', 'Chinese language learning and literature'),
        ('science', 'Science', 'General science subjects')
    """)


def downgrade() -> None:
    # Drop all tables in reverse order (respecting foreign key constraints)
    op.drop_table('cached_explanations')
    op.drop_table('gifts')
    op.drop_table('rewards')
    op.drop_table('topics')
    op.drop_table('class_notes')
    op.drop_table('homework')
    op.drop_table('test_results')
    op.drop_table('questions')
    op.drop_table('tests')
    op.drop_table('study_sessions')
    op.drop_table('subjects')
    op.drop_table('users')
