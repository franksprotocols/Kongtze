"""Seed default AI prompt templates for test generation"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.ai_prompt_template import AIPromptTemplate


async def seed_templates():
    """Seed default prompt templates"""
    print("=" * 60)
    print("SEEDING DEFAULT PROMPT TEMPLATES")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        # Check if templates already exist
        result = await db.execute(
            select(AIPromptTemplate).where(AIPromptTemplate.is_system == True)
        )
        existing = result.scalars().all()

        if existing:
            print(f"\n⚠️  Found {len(existing)} existing system templates.")
            print("Skipping seed to avoid duplicates.")
            return

        # Default templates to create
        templates = [
            {
                "template_name": "adaptive_test_generation",
                "template_type": "test_generation",
                "prompt_template": """You are an expert education AI creating a personalized test for a student.

{context}

TASK: Generate {num_questions} test questions at difficulty level {difficulty_level}/4.

REQUIREMENTS:
1. Questions must be appropriate for the student's age ({age}) and proficiency level
2. Focus on topics from recent class notes and homework
3. Address known weaknesses while building on strengths
4. Match the specified difficulty level consistently
5. Include a mix of question types: {question_types}

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_text": "Question text here",
      "question_type": "multiple_choice|true_false|short_answer|essay",
      "options": ["A", "B", "C", "D"],  // for multiple_choice only
      "correct_answer": "Correct answer",
      "points": 10,
      "explanation": "Why this is the correct answer"
    }}
  ]
}}

Generate the test now.""",
                "description": "Main template for adaptive test generation with student context",
                "is_active": True,
                "is_system": True
            },
            {
                "template_name": "note_based_test_generation",
                "template_type": "test_generation",
                "prompt_template": """You are an expert education AI creating a test based on class notes.

STUDENT PROFILE:
- Age: {age}
- Grade: {grade_level}
- Subject Proficiency: {subject_level}

CLASS NOTES:
{notes_content}

TASK: Generate {num_questions} questions at difficulty level {difficulty_level}/4 based on the class notes above.

REQUIREMENTS:
1. Questions must directly relate to topics covered in the notes
2. Test understanding of key concepts from the notes
3. Match the student's proficiency level
4. Include a mix of question types

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_text": "Question text here",
      "question_type": "multiple_choice|true_false|short_answer|essay",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "Correct answer",
      "points": 10,
      "explanation": "Why this is correct"
    }}
  ]
}}

Generate the test now.""",
                "description": "Template for generating tests based on class notes",
                "is_active": True,
                "is_system": True
            },
            {
                "template_name": "homework_based_test_generation",
                "template_type": "test_generation",
                "prompt_template": """You are an expert education AI creating a test based on homework assignments.

STUDENT PROFILE:
- Age: {age}
- Grade: {grade_level}
- Subject Proficiency: {subject_level}

HOMEWORK CONTENT:
{homework_content}

TASK: Generate {num_questions} questions at difficulty level {difficulty_level}/4 based on the homework above.

REQUIREMENTS:
1. Questions should test similar concepts to the homework
2. Vary the question format from the homework to test true understanding
3. Match the student's proficiency level
4. Progress from easier to harder questions

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_text": "Question text here",
      "question_type": "multiple_choice|true_false|short_answer|essay",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "Correct answer",
      "points": 10,
      "explanation": "Why this is correct"
    }}
  ]
}}

Generate the test now.""",
                "description": "Template for generating tests based on homework",
                "is_active": True,
                "is_system": True
            },
            {
                "template_name": "pure_ai_test_generation",
                "template_type": "test_generation",
                "prompt_template": """You are an expert education AI creating a test for a student.

STUDENT PROFILE:
- Age: {age}
- Grade: {grade_level}
- Subject: {subject_name}
- Proficiency Level: {subject_level}
- Strengths: {strengths}
- Weaknesses: {weaknesses}

TASK: Generate {num_questions} {subject_name} questions at difficulty level {difficulty_level}/4.

REQUIREMENTS:
1. Questions must be age-appropriate and match proficiency level
2. Cover a broad range of topics in {subject_name}
3. Address known weaknesses while building on strengths
4. Include a mix of question types
5. Ensure questions are clear and unambiguous

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_text": "Question text here",
      "question_type": "multiple_choice|true_false|short_answer|essay",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "Correct answer",
      "points": 10,
      "explanation": "Why this is correct"
    }}
  ]
}}

Generate the test now.""",
                "description": "Template for pure AI test generation without specific content",
                "is_active": True,
                "is_system": True
            },
            {
                "template_name": "schedule_generation",
                "template_type": "schedule_generation",
                "prompt_template": """You are an expert education AI creating a personalized study schedule.

STUDENT PROFILE:
{student_profile}

SUBJECTS:
{subjects}

SCHEDULE PARAMETERS:
- Start Date: {start_date}
- End Date: {end_date}
- Study Days: {study_days}
- Session Length: {session_length} minutes

ADAPTIVE DIFFICULTY LEVELS:
{adaptive_difficulties}

TASK: Create a balanced study schedule that:
1. Distributes subjects evenly across the week
2. Uses progressive difficulty (review → new concepts → challenge)
3. Considers the student's proficiency levels
4. Includes appropriate breaks and variety
5. Follows the adaptive difficulty recommendations

OUTPUT FORMAT (JSON):
{{
  "schedule": [
    {{
      "date": "YYYY-MM-DD",
      "subject_id": 1,
      "subject_name": "Mathematics",
      "session_type": "review|new_concepts|practice|challenge",
      "difficulty_level": 2,
      "topics": ["Topic 1", "Topic 2"],
      "notes": "Session notes"
    }}
  ]
}}

Generate the schedule now.""",
                "description": "Template for AI-powered schedule generation",
                "is_active": True,
                "is_system": True
            }
        ]

        # Create templates
        created_count = 0
        for template_data in templates:
            template = AIPromptTemplate(**template_data)
            db.add(template)
            created_count += 1
            print(f"✓ Created: {template_data['template_name']}")

        await db.commit()

        print(f"\n✅ Successfully created {created_count} system prompt templates")


if __name__ == "__main__":
    asyncio.run(seed_templates())

