"""Student Profile Service for managing student profiles"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.student_profile import StudentProfile
from app.models.user import User


class StudentProfileService:
    """Service for managing student profiles"""

    async def get_or_create_profile(
        self,
        user_id: int,
        db: AsyncSession
    ) -> StudentProfile:
        """
        Get existing profile or create default profile for user

        Args:
            user_id: User ID
            db: Database session

        Returns:
            StudentProfile object
        """
        # Check if profile exists
        result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if profile:
            return profile

        # Create default profile based on tech spec requirements
        profile = StudentProfile(
            user_id=user_id,
            age=10,
            grade_level="Primary 4",
            school_name="Dulwich College Singapore",
            math_proficiency=4,  # Advanced
            english_proficiency=4,  # Advanced
            chinese_proficiency=2,  # Average
            science_proficiency=3,  # Intermediate
            strengths_weaknesses={
                "strengths": [
                    "Strong mathematical reasoning",
                    "Excellent English comprehension and vocabulary",
                    "Quick learner in science concepts"
                ],
                "weaknesses": [
                    "Chinese writing needs improvement",
                    "Struggles with Chinese character memorization",
                    "Needs more practice with Chinese composition"
                ]
            },
            learning_pace="fast",
            notes="Default profile created. Please update with accurate information."
        )

        db.add(profile)
        await db.commit()
        await db.refresh(profile)

        return profile

    async def update_profile(
        self,
        user_id: int,
        db: AsyncSession,
        **updates
    ) -> StudentProfile:
        """
        Update student profile

        Args:
            user_id: User ID
            db: Database session
            **updates: Fields to update

        Returns:
            Updated StudentProfile object
        """
        result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError("Profile not found")

        # Update fields
        for field, value in updates.items():
            if hasattr(profile, field):
                setattr(profile, field, value)

        await db.commit()
        await db.refresh(profile)

        return profile


# Create singleton instance
student_profile_service = StudentProfileService()
