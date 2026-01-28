"""Seed default student profile for existing user"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.student_profile import StudentProfile


async def seed_default_profile():
    """Create default student profile for the first user"""
    async with AsyncSessionLocal() as db:
        # Get the first user (assuming this is the student)
        result = await db.execute(select(User).limit(1))
        user = result.scalar_one_or_none()

        if not user:
            print("No user found in database. Please create a user first.")
            return

        # Check if profile already exists
        result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user.user_id)
        )
        existing_profile = result.scalar_one_or_none()

        if existing_profile:
            print(f"Profile already exists for user {user.name} (ID: {user.user_id})")
            return

        # Create default profile based on requirements:
        # 10 years old, Dulwich College Singapore
        # Advanced math/English (AMC-style), Average Chinese with weak writing
        profile = StudentProfile(
            user_id=user.user_id,
            age=10,
            grade_level="Grade 5",
            school_name="Dulwich College Singapore",
            math_level="Advanced (AMC-style)",
            english_level="Advanced",
            chinese_level="Average",
            strengths=[
                "Advanced mathematics",
                "English comprehension",
                "Chinese listening",
                "Chinese speaking",
                "Problem-solving"
            ],
            weaknesses=[
                "Chinese writing",
                "Chinese character recognition"
            ],
            learning_pace="Fast",
            preferred_question_types=[
                "Multiple choice",
                "Problem-solving",
                "Application questions"
            ],
            notes="Student excels in math and English. Needs additional support in Chinese writing skills."
        )

        db.add(profile)
        await db.commit()
        await db.refresh(profile)

        print(f"✓ Created default profile for user {user.name} (ID: {user.user_id})")
        print(f"  Profile ID: {profile.profile_id}")
        print(f"  Age: {profile.age}")
        print(f"  School: {profile.school_name}")
        print(f"  Math Level: {profile.math_level}")
        print(f"  English Level: {profile.english_level}")
        print(f"  Chinese Level: {profile.chinese_level}")


if __name__ == "__main__":
    asyncio.run(seed_default_profile())
