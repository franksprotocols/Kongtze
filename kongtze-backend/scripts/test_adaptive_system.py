"""Test script for adaptive test generation system"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.core.database import AsyncSessionLocal
from app.models.student_profile import StudentProfile
from app.models.student_performance_analytics import StudentPerformanceAnalytics
from app.models.ai_prompt_template import AIPromptTemplate
from app.services.test_context_builder import test_context_builder
from app.services.adaptive_difficulty_service import adaptive_difficulty_service


async def test_database_tables():
    """Test that all new tables exist"""
    print("=" * 60)
    print("TEST 1: Database Tables")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        try:
            # Test student_profiles table
            result = await db.execute(text("SELECT COUNT(*) FROM student_profiles"))
            count = result.scalar()
            print(f"✓ student_profiles table exists ({count} records)")

            # Test student_performance_analytics table
            result = await db.execute(text("SELECT COUNT(*) FROM student_performance_analytics"))
            count = result.scalar()
            print(f"✓ student_performance_analytics table exists ({count} records)")

            # Test ai_prompt_templates table
            result = await db.execute(text("SELECT COUNT(*) FROM ai_prompt_templates"))
            count = result.scalar()
            print(f"✓ ai_prompt_templates table exists ({count} records)")

            return True
        except Exception as e:
            print(f"✗ Database table test failed: {e}")
            return False


async def test_student_profile():
    """Test student profile retrieval"""
    print("\n" + "=" * 60)
    print("TEST 2: Student Profile")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(select(StudentProfile).limit(1))
            profile = result.scalar_one_or_none()

            if profile:
                print(f"✓ Found student profile:")
                print(f"  - User ID: {profile.user_id}")
                print(f"  - Age: {profile.age}")
                print(f"  - School: {profile.school_name}")
                print(f"  - Math Level: {profile.math_level}")
                print(f"  - English Level: {profile.english_level}")
                print(f"  - Chinese Level: {profile.chinese_level}")
                print(f"  - Strengths: {profile.strengths}")
                print(f"  - Weaknesses: {profile.weaknesses}")
                return True
            else:
                print("✗ No student profile found")
                return False
        except Exception as e:
            print(f"✗ Student profile test failed: {e}")
            return False


async def test_adaptive_difficulty():
    """Test adaptive difficulty calculation"""
    print("\n" + "=" * 60)
    print("TEST 3: Adaptive Difficulty Service")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        try:
            # Get first user
            result = await db.execute(text("SELECT user_id FROM users LIMIT 1"))
            user_id = result.scalar_one_or_none()

            if not user_id:
                print("✗ No user found for testing")
                return False

            # Get first subject
            result = await db.execute(text("SELECT subject_id FROM subjects LIMIT 1"))
            subject_id = result.scalar_one_or_none()

            if not subject_id:
                print("✗ No subject found for testing")
                return False

            # Test adaptive difficulty calculation
            recommended_difficulty = await adaptive_difficulty_service.calculate_recommended_difficulty(
                user_id=user_id,
                subject_id=subject_id,
                db=db
            )
            print(f"✓ Adaptive difficulty calculated: Level {recommended_difficulty}")

            # Test dynamic question count
            question_count = await adaptive_difficulty_service.calculate_dynamic_question_count(
                user_id=user_id,
                subject_id=subject_id,
                session_length_minutes=30,
                difficulty_level=recommended_difficulty,
                db=db
            )
            print(f"✓ Dynamic question count calculated: {question_count} questions")

            # Test individual time limits
            time_limits = adaptive_difficulty_service.calculate_individual_time_limits(
                question_count=question_count,
                session_length_minutes=30,
                difficulty_level=recommended_difficulty
            )
            print(f"✓ Individual time limits calculated: {time_limits[:5]}... (showing first 5)")
            print(f"  Total time: {sum(time_limits)} seconds ({sum(time_limits)/60:.1f} minutes)")

            return True
        except Exception as e:
            print(f"✗ Adaptive difficulty test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def test_context_builder_service():
    """Test context builder service"""
    print("\n" + "=" * 60)
    print("TEST 4: Test Context Builder")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        try:
            # Get first user
            result = await db.execute(text("SELECT user_id FROM users LIMIT 1"))
            user_id = result.scalar_one_or_none()

            if not user_id:
                print("✗ No user found for testing")
                return False

            # Get first subject
            result = await db.execute(text("SELECT subject_id FROM subjects LIMIT 1"))
            subject_id = result.scalar_one_or_none()

            if not subject_id:
                print("✗ No subject found for testing")
                return False

            # Build context
            context = await test_context_builder.build_context(
                user_id=user_id,
                subject_id=subject_id,
                db=db
            )

            print(f"✓ Context built successfully")
            print(f"  Context length: {len(context)} characters")
            print(f"  Preview (first 500 chars):")
            print(f"  {context[:500]}...")

            # Test automatic content selection
            content_ids = await test_context_builder.get_relevant_content_ids(
                user_id=user_id,
                subject_id=subject_id,
                db=db
            )

            print(f"\n✓ Automatic content selection:")
            print(f"  Note IDs: {content_ids['note_ids']}")
            print(f"  Homework IDs: {content_ids['homework_ids']}")

            return True
        except Exception as e:
            print(f"✗ Context builder test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def test_prompt_templates():
    """Test prompt template model"""
    print("\n" + "=" * 60)
    print("TEST 5: Prompt Templates")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        try:
            # Create a test template
            test_template = AIPromptTemplate(
                template_name="test_generation_test",
                template_type="test_generation",
                prompt_template="Generate {num_questions} questions about {subject} at {difficulty_level} difficulty.",
                description="Test template for verification",
                is_active=True,
                is_system=False
            )

            db.add(test_template)
            await db.commit()
            await db.refresh(test_template)

            print(f"✓ Created test prompt template (ID: {test_template.template_id})")

            # Test template rendering
            rendered = test_template.prompt_template.format(
                num_questions=10,
                subject="Mathematics",
                difficulty_level="intermediate"
            )
            print(f"✓ Template rendering works:")
            print(f"  {rendered}")

            # Clean up
            await db.delete(test_template)
            await db.commit()
            print(f"✓ Cleaned up test template")

            return True
        except Exception as e:
            print(f"✗ Prompt template test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("ADAPTIVE TEST GENERATION SYSTEM - TEST SUITE")
    print("=" * 60 + "\n")

    results = []

    # Run tests
    results.append(("Database Tables", await test_database_tables()))
    results.append(("Student Profile", await test_student_profile()))
    results.append(("Adaptive Difficulty", await test_adaptive_difficulty()))
    results.append(("Context Builder", await test_context_builder_service()))
    results.append(("Prompt Templates", await test_prompt_templates()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The adaptive test generation system is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
