"""Seed default AI prompt templates"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import engine, get_db
from app.models.ai_prompt_template import AIPromptTemplate


async def seed_prompt_templates():
    """Seed default AI prompt templates"""

    async with engine.begin() as conn:
        # Create async session
        from sqlalchemy.ext.asyncio import async_sessionmaker
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as db:
            # Check if templates already exist
            result = await db.execute(select(AIPromptTemplate))
            existing = result.scalars().all()

            if existing:
                print(f"Found {len(existing)} existing templates. Skipping seed.")
                return

            # Default templates
            templates = [
                {
                    "template_name": "Test Question Generation",
                    "template_type": "test_generation",
                    "description": "Generate test questions based on subject, difficulty, and context",
                    "prompt_template": """Generate {num_questions} test questions for a {age}-year-old student in {grade_level} studying {subject_name}.

Student Profile:
- Subject Proficiency: {subject_level}
- Strengths: {strengths}
- Weaknesses: {weaknesses}

Difficulty Level: {difficulty_level} (1=Beginner, 2=Intermediate, 3=Advanced, 4=Expert)

Context and Learning Materials:
{context}

Requirements:
1. Generate exactly {num_questions} multiple-choice questions
2. Each question should have 4 options (A, B, C, D)
3. Questions should be appropriate for the student's age and proficiency level
4. Focus on areas where the student needs improvement
5. Include a mix of question types: {question_types}
6. Questions should test understanding, not just memorization

Return ONLY a JSON array with this exact structure:
[
  {{
    "question_text": "Question text here",
    "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
    "correct_answer": "A"
  }}
]

No markdown, no explanation, just the JSON array.""",
                    "is_system": True,
                    "is_active": True
                },
                {
                    "template_name": "Schedule Generation",
                    "template_type": "schedule_generation",
                    "description": "Generate optimized weekly study schedule",
                    "prompt_template": """Generate an optimized weekly study schedule with the following requirements:

Subjects to study: {subjects}
Target study hours per day: {hours_per_day} hours
Time window: {start_time} to {end_time}
Goals: {goals}

ADAPTIVE DIFFICULTY GUIDANCE:
{adaptive_context}

PROGRESSIVE DIFFICULTY CURVE:
- Early week (Monday-Tuesday): Focus on review and reinforcement
- Mid week (Wednesday-Thursday): Introduce new concepts at recommended difficulty
- Late week (Friday-Sunday): Challenge sessions and practice

IMPORTANT CONSTRAINTS:
1. ALL sessions MUST be within the time window {start_time} to {end_time}
2. AVOID dinner time: 19:00-19:40 (7:00 PM - 7:40 PM)
3. Session durations should be 30 or 45 minutes ONLY
4. Maximum 3 sessions per day
5. Each subject can only appear ONCE per day
6. Distribute subjects evenly across the week
7. Include rest days (1-2 days with no or minimal study)
8. WEEKDAY SESSIONS (Monday-Friday): 1 session BEFORE dinner + 2 sessions AFTER dinner
9. WEEKEND SESSIONS (Saturday-Sunday): 2 sessions between 11:00 AM and 4:00 PM

Return ONLY a JSON array with this exact structure:
[
  {{
    "day_of_week": 0,
    "subject_name": "Math",
    "start_time": "14:00:00",
    "duration_minutes": 45
  }}
]

day_of_week: 0=Monday, 1=Tuesday, ..., 6=Sunday
No markdown, no explanation, just the JSON array.""",
                    "is_system": True,
                    "is_active": True
                },
                {
                    "template_name": "Homework Analysis",
                    "template_type": "homework_analysis",
                    "description": "Analyze homework and provide feedback",
                    "prompt_template": """Analyze the following homework submission for a {age}-year-old student in {grade_level}.

Subject: {subject_name}
Student Proficiency: {subject_level}

Homework Content:
{homework_content}

Please provide:
1. Overall assessment (score out of 100)
2. Strengths demonstrated
3. Areas for improvement
4. Specific feedback on errors or misconceptions
5. Recommendations for further practice

Format your response as JSON:
{{
  "score": 85,
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["area 1", "area 2"],
  "feedback": "Detailed feedback here",
  "recommendations": ["recommendation 1", "recommendation 2"]
}}""",
                    "is_system": True,
                    "is_active": True
                }
            ]

            # Create templates
            for template_data in templates:
                template = AIPromptTemplate(**template_data)
                db.add(template)

            await db.commit()
            print(f"Successfully seeded {len(templates)} prompt templates")


if __name__ == "__main__":
    asyncio.run(seed_prompt_templates())
