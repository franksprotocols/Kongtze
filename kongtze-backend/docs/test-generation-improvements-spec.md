# Test Generation System Improvements - Technical Specification

**Date:** 2026-01-28
**Status:** Draft
**Author:** Technical Specification

## Executive Summary

This specification outlines improvements to the Kongtze test generation system to make it adaptive, personalized, and context-aware. The system will dynamically adjust question difficulty, time limits, and content based on student performance history, school notes, homework assignments, and individual student profiles.

## 1. Dynamic Question Time Limits

### Current State
- Fixed time limit per test (e.g., 30 minutes total)
- Fixed number of questions (e.g., 10 questions)
- No individual question time limits
- No adaptation based on student performance

### Proposed Changes

#### 1.1 Individual Question Time Limits
**Database Schema Changes:**
```sql
-- Already exists in questions table:
-- time_limit_seconds: int (currently defaults to 60)

-- Need to add to test_results table:
ALTER TABLE test_results ADD COLUMN question_timings JSON;
-- Format: {"question_id": seconds_taken, ...}
```

#### 1.2 Adaptive Time Allocation Algorithm
**Logic:**
1. Calculate available time for session (from calendar schedule)
2. Analyze student's historical performance per subject/difficulty
3. Allocate time per question based on:
   - Base difficulty (1-4 scale)
   - Student's average time for similar questions
   - Student's success rate at this difficulty
   - Question type complexity

**Formula:**
```python
base_time = {
    1: 45,  # Beginner: 45 seconds
    2: 60,  # Intermediate: 60 seconds
    3: 90,  # Advanced: 90 seconds
    4: 120  # Expert: 120 seconds
}

student_performance_factor = calculate_performance_factor(
    student_history,
    subject,
    difficulty_level
)

question_time_limit = base_time[difficulty] * student_performance_factor
# student_performance_factor ranges from 0.7 to 1.5
# - 0.7 for students who consistently answer quickly and correctly
# - 1.5 for students who need more time
```

#### 1.3 Dynamic Question Count
**Logic:**
1. Start with session time limit (e.g., 45 minutes max per session)
2. Reserve 10% for transitions and instructions
3. Generate questions until time budget is filled
4. Minimum 5 questions, maximum 20 questions per test

**Implementation:**
```python
def calculate_question_count(
    session_duration_minutes: int,
    difficulty_level: int,
    student_performance_history: dict
) -> int:
    available_time = session_duration_minutes * 60 * 0.9  # 90% of session
    avg_question_time = estimate_avg_question_time(
        difficulty_level,
        student_performance_history
    )
    question_count = int(available_time / avg_question_time)
    return max(5, min(20, question_count))
```

## 2. Test History as AI Context

### Current State
- Test results are stored but not used for future generation
- No adaptive difficulty adjustment
- No learning from student performance patterns

### Proposed Changes

#### 2.1 Performance Analytics Storage
**New Database Table:**
```sql
CREATE TABLE student_performance_analytics (
    analytics_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    subject_id INTEGER REFERENCES subjects(subject_id),

    -- Performance metrics
    total_tests_taken INTEGER DEFAULT 0,
    average_score DECIMAL(5,2),  -- 0-100
    average_time_per_question INTEGER,  -- seconds

    -- Difficulty progression
    current_difficulty_level INTEGER,  -- 1-4
    recommended_difficulty_level INTEGER,  -- 1-4
    difficulty_trend VARCHAR(20),  -- 'improving', 'stable', 'declining'

    -- Time period
    period_start DATE,
    period_end DATE,

    -- Detailed breakdown by difficulty
    difficulty_breakdown JSON,
    -- Format: {
    --   "1": {"tests": 5, "avg_score": 95, "avg_time": 40},
    --   "2": {"tests": 3, "avg_score": 80, "avg_time": 55},
    --   ...
    -- }

    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_student_performance ON student_performance_analytics(user_id, subject_id);
```

#### 2.2 AI Context Builder
**Service: `app/services/test_context_builder.py`**
```python
class TestContextBuilder:
    async def build_context(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession
    ) -> str:
        """Build comprehensive context for AI test generation"""

        # 1. Get recent test history (last 10 tests)
        recent_tests = await self.get_recent_tests(user_id, subject_id, db)

        # 2. Get performance analytics
        analytics = await self.get_performance_analytics(user_id, subject_id, db)

        # 3. Get student profile
        profile = await self.get_student_profile(user_id, db)

        # 4. Get recent notes (last 2 weeks)
        notes = await self.get_recent_notes(user_id, subject_id, db)

        # 5. Build context string
        context = self._format_context(
            recent_tests, analytics, profile, notes
        )

        return context
```

#### 2.3 Adaptive Difficulty Algorithm
**Logic:**
```python
def calculate_next_difficulty(
    current_difficulty: int,
    recent_scores: List[int],  # Last 5 test scores
    recent_times: List[int],   # Time taken vs allocated
    subject: str
) -> int:
    """
    Adjust difficulty based on performance:
    - If consistently scoring 90%+ and finishing early: increase difficulty
    - If scoring 70-89% and finishing on time: maintain difficulty
    - If scoring <70% or running out of time: decrease difficulty
    """
    avg_score = sum(recent_scores) / len(recent_scores)
    avg_time_ratio = sum(recent_times) / len(recent_times)  # actual/allocated

    if avg_score >= 90 and avg_time_ratio < 0.8:
        # Excelling - increase difficulty
        return min(4, current_difficulty + 1)
    elif avg_score < 70 or avg_time_ratio > 1.1:
        # Struggling - decrease difficulty
        return max(1, current_difficulty - 1)
    else:
        # Appropriate level - maintain
        return current_difficulty
```

## 3. Student Profile Context

### Current State
- No student profile information
- Generic test generation for all students
- No personalization based on student characteristics

### Proposed Changes

#### 3.1 Student Profile Schema
**New Database Table:**
```sql
CREATE TABLE student_profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) UNIQUE,

    -- Basic info
    age INTEGER,
    grade_level VARCHAR(50),
    school_name VARCHAR(255),

    -- Subject proficiency levels
    math_level VARCHAR(50),  -- 'beginner', 'intermediate', 'advanced', 'expert'
    english_level VARCHAR(50),
    chinese_level VARCHAR(50),

    -- Specific strengths/weaknesses
    strengths JSON,  -- ["mental_math", "geometry", "problem_solving"]
    weaknesses JSON,  -- ["chinese_writing", "essay_structure"]

    -- Learning style
    learning_pace VARCHAR(50),  -- 'fast', 'moderate', 'slow'
    preferred_question_types JSON,  -- ["multiple_choice", "short_answer"]

    -- Special considerations
    notes TEXT,  -- Free-form notes about student

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.2 Default Profile for Current Student
**Initial Data:**
```json
{
  "age": 10,
  "grade_level": "Primary 5",
  "school_name": "Dulwich College Singapore",
  "math_level": "advanced",
  "english_level": "advanced",
  "chinese_level": "intermediate",
  "strengths": [
    "AMC-style math problems",
    "English comprehension",
    "Chinese listening",
    "Chinese speaking"
  ],
  "weaknesses": [
    "Chinese writing",
    "Chinese character recognition",
    "Essay composition in Chinese"
  ],
  "learning_pace": "fast",
  "preferred_question_types": ["multiple_choice", "short_answer"],
  "notes": "Student is 10 years old at Dulwich College Singapore. Math and English are advanced (AMC-style math). Chinese is average overall but fluent in speaking/listening, weak in writing. Chinese tests should include article writing and listening-to-write exercises."
}
```

#### 3.3 Profile-Aware Test Generation
**AI Prompt Enhancement:**
```python
def build_profile_context(profile: StudentProfile) -> str:
    return f"""
Student Profile:
- Age: {profile.age} years old
- School: {profile.school_name}
- Grade: {profile.grade_level}

Subject Proficiency:
- Math: {profile.math_level} (strengths: {', '.join(profile.strengths_math)})
- English: {profile.english_level}
- Chinese: {profile.chinese_level} (weak in writing, strong in listening/speaking)

Special Considerations:
{profile.notes}

Please generate questions that:
1. Match the student's proficiency level
2. Address known weaknesses for improvement
3. Include appropriate question types for this student
4. For Chinese: Include writing exercises and listening comprehension
"""
```

## 4. Weekly Notes and Homework as Context

### Current State
- Notes are stored but not automatically used for test generation
- Homework is stored but not used as context
- Manual selection of notes when creating tests
- No automatic relevance matching

### Proposed Changes

#### 4.1 Automatic Note Selection
**Logic:**
```python
async def get_relevant_notes(
    user_id: int,
    subject_id: int,
    weeks_back: int = 2,
    db: AsyncSession
) -> List[ClassNote]:
    """
    Get notes from the last N weeks for a subject
    """
    cutoff_date = datetime.now() - timedelta(weeks=weeks_back)

    result = await db.execute(
        select(ClassNote)
        .where(
            and_(
                ClassNote.user_id == user_id,
                ClassNote.subject_id == subject_id,
                ClassNote.created_at >= cutoff_date
            )
        )
        .order_by(ClassNote.created_at.desc())
    )

    return result.scalars().all()
```

#### 4.2 Automatic Homework Selection
**Logic:**
```python
async def get_relevant_homework(
    user_id: int,
    subject_id: int,
    weeks_back: int = 2,
    db: AsyncSession
) -> List[Homework]:
    """
    Get homework from the last N weeks for a subject
    """
    cutoff_date = datetime.now() - timedelta(weeks=weeks_back)

    result = await db.execute(
        select(Homework)
        .where(
            and_(
                Homework.user_id == user_id,
                Homework.subject_id == subject_id,
                Homework.created_at >= cutoff_date
            )
        )
        .order_by(Homework.created_at.desc())
    )

    return result.scalars().all()
```

#### 4.3 Combined Context Formatting
**Implementation:**
```python
def format_school_context(
    notes: List[ClassNote],
    homework: List[Homework]
) -> str:
    """
    Format both notes and homework into a unified context
    """
    context_parts = []

    # Add notes context
    if notes:
        context_parts.append("=== Recent Class Notes (Last 2 Weeks) ===")
        for i, note in enumerate(notes, 1):
            context_parts.append(f"""
Note {i}: {note.title}
Date: {note.created_at.strftime('%Y-%m-%d')}
Content Summary:
{note.ocr_text[:500]}...  # First 500 chars
---
""")
    else:
        context_parts.append("No recent class notes available.")

    context_parts.append("\n")

    # Add homework context
    if homework:
        context_parts.append("=== Recent Homework (Last 2 Weeks) ===")
        for i, hw in enumerate(homework, 1):
            context_parts.append(f"""
Homework {i}: {hw.title}
Date: {hw.created_at.strftime('%Y-%m-%d')}
Status: {hw.status}
Content Summary:
{hw.ocr_text[:500]}...  # First 500 chars
---
""")
    else:
        context_parts.append("No recent homework available.")

    context_parts.append("""

IMPORTANT: Please generate test questions that are relevant to these recent class topics and homework assignments.
- Questions should test understanding of concepts covered in the notes
- Questions should align with the difficulty and style of recent homework
- Ensure questions help reinforce what the student is currently learning in school
""")

    return "\n".join(context_parts)
```

#### 4.4 Enhanced Context Builder
**Updated Service:**
```python
class TestContextBuilder:
    async def build_context(
        self,
        user_id: int,
        subject_id: int,
        db: AsyncSession
    ) -> str:
        """Build comprehensive context for AI test generation"""

        # 1. Get recent test history (last 10 tests)
        recent_tests = await self.get_recent_tests(user_id, subject_id, db)

        # 2. Get performance analytics
        analytics = await self.get_performance_analytics(user_id, subject_id, db)

        # 3. Get student profile
        profile = await self.get_student_profile(user_id, db)

        # 4. Get recent notes (last 2 weeks)
        notes = await self.get_recent_notes(user_id, subject_id, db)

        # 5. Get recent homework (last 2 weeks) - NEW
        homework = await self.get_recent_homework(user_id, subject_id, db)

        # 6. Build context string
        context = self._format_context(
            recent_tests, analytics, profile, notes, homework
        )

        return context
```

## 5. Dynamic Difficulty and Question Count in Calendar Generation

### Current State
- Calendar generation creates tests with fixed difficulty and question count
- No variation based on student progress or session length
- Difficulty level is set once and doesn't adapt

### Proposed Changes

#### 5.1 Calendar Test Generation Enhancement
**Modified API Endpoint: `POST /api/calendar/generate`**

**Current Request:**
```json
{
  "subject_id": 1,
  "start_date": "2026-02-01",
  "end_date": "2026-02-28",
  "difficulty_level": 2,
  "questions_per_test": 10
}
```

**New Request:**
```json
{
  "subject_id": 1,
  "start_date": "2026-02-01",
  "end_date": "2026-02-28",
  "adaptive_difficulty": true,  // NEW: Use adaptive difficulty
  "initial_difficulty_level": 2,  // Starting point
  "adaptive_question_count": true,  // NEW: Adjust based on session length
  "session_constraints": {
    "max_duration_minutes": 45,
    "min_questions": 5,
    "max_questions": 20
  }
}
```

#### 5.2 Adaptive Calendar Generation Logic
**Implementation:**
```python
async def generate_adaptive_calendar(
    user_id: int,
    subject_id: int,
    start_date: date,
    end_date: date,
    initial_difficulty: int,
    db: AsyncSession
) -> List[ScheduledTest]:
    """
    Generate calendar with adaptive difficulty progression
    """
    # Get student's current performance level
    analytics = await get_performance_analytics(user_id, subject_id, db)
    current_difficulty = analytics.recommended_difficulty_level or initial_difficulty

    scheduled_tests = []
    current_date = start_date

    while current_date <= end_date:
        # Get available time slots for this date
        slots = await get_available_slots(user_id, current_date, db)

        for slot in slots:
            # Calculate appropriate difficulty for this test
            test_difficulty = calculate_progressive_difficulty(
                current_difficulty,
                len(scheduled_tests),  # Test number in sequence
                analytics
            )

            # Calculate question count based on slot duration
            question_count = calculate_question_count(
                slot.duration_minutes,
                test_difficulty,
                analytics
            )

            # Create scheduled test
            test = ScheduledTest(
                user_id=user_id,
                subject_id=subject_id,
                scheduled_date=current_date,
                scheduled_time=slot.start_time,
                difficulty_level=test_difficulty,
                total_questions=question_count,
                time_limit_minutes=slot.duration_minutes
            )

            scheduled_tests.append(test)

        current_date += timedelta(days=1)

    return scheduled_tests
```

#### 5.3 Progressive Difficulty Curve
**Logic:**
```python
def calculate_progressive_difficulty(
    base_difficulty: int,
    test_sequence_number: int,
    analytics: PerformanceAnalytics
) -> int:
    """
    Gradually increase difficulty over time if student is performing well
    """
    # Every 5 tests, consider increasing difficulty
    if test_sequence_number > 0 and test_sequence_number % 5 == 0:
        if analytics.difficulty_trend == 'improving':
            return min(4, base_difficulty + 1)
        elif analytics.difficulty_trend == 'declining':
            return max(1, base_difficulty - 1)

    return base_difficulty
```

## 6. Prompt Configuration UI

### Current State
- AI prompts are hardcoded in service layer
- No visibility into what prompts are being sent to AI
- No way to adjust prompts without code changes

### Proposed Changes

#### 6.1 Prompt Template Storage
**New Database Table:**
```sql
CREATE TABLE ai_prompt_templates (
    template_id SERIAL PRIMARY KEY,
    template_name VARCHAR(100) UNIQUE NOT NULL,
    template_type VARCHAR(50) NOT NULL,  -- 'test_generation', 'calendar_generation'

    -- Template sections
    system_prompt TEXT,
    user_prompt_template TEXT,

    -- Variables used in template
    variables JSON,  -- ["subject", "difficulty_level", "student_profile", ...]

    -- Metadata
    is_active BOOLEAN DEFAULT true,
    version INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Default test generation template
INSERT INTO ai_prompt_templates (template_name, template_type, system_prompt, user_prompt_template, variables)
VALUES (
    'default_test_generation',
    'test_generation',
    'You are an expert educational content creator specializing in creating age-appropriate test questions for students.',
    'Generate {num_questions} test questions for {subject} at difficulty level {difficulty_level}...',
    '["subject", "difficulty_level", "num_questions", "student_profile", "notes_context", "performance_history"]'
);
```

#### 6.2 Prompt Configuration API
**New Endpoints:**
```python
# GET /api/admin/prompts
# List all prompt templates

# GET /api/admin/prompts/{template_id}
# Get specific template with current variable values

# PUT /api/admin/prompts/{template_id}
# Update template

# POST /api/admin/prompts/preview
# Preview rendered prompt with sample data
```

#### 6.3 Prompt Configuration UI
**New Frontend Page: `/dashboard/admin/prompts`**

**Features:**
1. **Template List View**
   - Show all available templates
   - Active/inactive status
   - Last modified date
   - Version history

2. **Template Editor**
   - System prompt editor (textarea)
   - User prompt template editor (textarea with variable highlighting)
   - Variable list with descriptions
   - Real-time preview with sample data

3. **Variable Configuration**
   - List of all variables used in prompts
   - Current values/sources for each variable
   - Ability to modify default values
   - Data source mapping (e.g., "student_profile" → student_profiles table)

4. **Prompt Preview**
   - Select a student
   - Select a subject
   - See the complete rendered prompt that would be sent to AI
   - Test prompt with AI and see response

**UI Mockup Structure:**
```
┌─────────────────────────────────────────────────────────┐
│ Prompt Configuration                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Template: Test Generation (default)          [Active ✓] │
│                                                          │
│ System Prompt:                                           │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ You are an expert educational content creator...    │ │
│ │                                                      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ User Prompt Template:                                    │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Generate {num_questions} questions for {subject}    │ │
│ │ at difficulty level {difficulty_level}.             │ │
│ │                                                      │ │
│ │ Student Profile:                                     │ │
│ │ {student_profile}                                    │ │
│ │                                                      │ │
│ │ Recent Performance:                                  │ │
│ │ {performance_history}                                │ │
│ │                                                      │ │
│ │ Class Notes Context:                                 │ │
│ │ {notes_context}                                      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ Variables:                                               │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ • num_questions: Number of questions to generate    │ │
│ │ • subject: Subject name                             │ │
│ │ • difficulty_level: 1-4 scale                       │ │
│ │ • student_profile: Student background info          │ │
│ │ • performance_history: Recent test results          │ │
│ │ • notes_context: Recent class notes                 │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [Preview Prompt] [Save Changes] [Reset to Default]      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 6.4 Prompt Preview Feature
**Implementation:**
```python
@router.post("/admin/prompts/preview")
async def preview_prompt(
    template_id: int,
    preview_data: PromptPreviewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Preview what the actual prompt would look like with real data
    """
    # Get template
    template = await get_template(template_id, db)

    # Build context with real data
    context = await build_test_context(
        user_id=preview_data.user_id,
        subject_id=preview_data.subject_id,
        db=db
    )

    # Render template
    rendered_prompt = render_template(template, context)

    return {
        "system_prompt": template.system_prompt,
        "user_prompt": rendered_prompt,
        "variables_used": context.keys(),
        "character_count": len(rendered_prompt),
        "estimated_tokens": len(rendered_prompt) // 4  # Rough estimate
    }
```

## Implementation Plan

### Phase 1: Foundation (Week 1-2)
1. Create student_profiles table and API
2. Create student_performance_analytics table
3. Implement TestContextBuilder service
4. Add profile for current student

### Phase 2: Adaptive Logic (Week 3-4)
5. Implement adaptive difficulty algorithm
6. Implement dynamic question count calculation
7. Implement individual question time limits
8. Update test generation to use context

### Phase 3: Calendar Integration (Week 5)
9. Update calendar generation to use adaptive difficulty
10. Implement progressive difficulty curve
11. Add automatic note and homework selection for context

### Phase 4: Prompt Configuration (Week 6-7)
12. Create ai_prompt_templates table
13. Build prompt configuration API
14. Build prompt configuration UI
15. Implement prompt preview feature

### Phase 5: Testing & Refinement (Week 8)
16. End-to-end testing
17. Performance tuning
18. UI/UX refinement
19. Documentation

## Technical Considerations

### Performance
- Cache student analytics (refresh every 24 hours)
- Limit note context to last 2 weeks (configurable)
- Implement pagination for test history
- Use database indexes on frequently queried fields

### Security
- Prompt configuration should be admin-only
- Validate all template variables before rendering
- Sanitize user input in prompts
- Rate limit AI API calls

### Data Privacy
- Student profiles contain sensitive information
- Implement proper access controls
- Consider data retention policies
- GDPR compliance for student data

### AI Token Management
- Monitor prompt length (context can get large)
- Implement token counting before API calls
- Set maximum context length limits
- Fallback to shorter context if needed

## Success Metrics

1. **Adaptive Difficulty**
   - Student performance improves over time
   - Difficulty level increases as student improves
   - Fewer tests with scores <70% or >95%

2. **Time Management**
   - 90%+ of students complete tests within time limit
   - Average time utilization: 80-90% of allocated time
   - Fewer timeout incidents

3. **Relevance**
   - Questions align with recent class notes and homework
   - Student/parent feedback on question relevance
   - Improved engagement with tests

4. **Personalization**
   - Questions match student's proficiency level
   - Appropriate question types for student
   - Addresses known weaknesses

## Open Questions

1. How often should we recalculate performance analytics?
2. What's the minimum number of tests needed before adaptive difficulty kicks in?
3. Should parents/teachers be able to override AI-recommended difficulty?
4. How do we handle multiple students with different profiles in the same household?
5. What's the fallback if AI generation fails or produces inappropriate questions?

## Next Steps

1. Review and approve this specification
2. Create detailed database migration scripts
3. Set up development environment for testing
4. Begin Phase 1 implementation
5. Schedule regular check-ins for progress review
