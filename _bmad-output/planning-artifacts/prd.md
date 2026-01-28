---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'complete']
inputDocuments: ['_bmad/_memory/project-vision-and-requirements.md']
workflowType: 'prd'
briefCount: 0
researchCount: 0
brainstormingCount: 0
projectDocsCount: 0
memoryDocsCount: 1
classification:
  projectType: 'Web Application (Progressive Web App)'
  domain: 'Education Technology (EdTech)'
  complexity: 'Medium-High'
  projectContext: 'greenfield'
---

# Product Requirements Document - Kongtze

**Author:** Frankhu  
**Date:** 2026-01-21  
**Version:** 1.1  
**Last Updated:** 2026-01-21  
**Project Type:** Education Technology - AI-Powered Study Platform  
**Status:** In Review

**Change Log:**
- v1.1 (2026-01-21): Added Section 5.4 - Class Notes Upload & Curriculum Tracking feature
- v1.0 (2026-01-21): Initial PRD creation

---

## 1. Executive Summary

Kongtze is an AI-powered education platform designed to help a 10-year-old student excel academically through personalized study planning, adaptive testing, and gamified learning. The platform combines intelligent scheduling, difficulty-adaptive assessments, and reward mechanisms to create an engaging learning experience tailored to the student's strengths and weaknesses.

### Key Highlights
- **Personalized Learning:** AI adapts test difficulty and time limits based on student performance
- **Dual Interface:** Kid-friendly testing interface + Parent dashboard for oversight
- **Gamification:** Points, rewards, and lucky draw system to maintain motivation
- **Multi-Subject Support:** Math, English, Chinese, Science with extensible architecture
- **Homework Integration:** Upload and digitize school homework photos for testing
- **Class Notes Integration:** Upload daily class notes to inform AI test generation based on current curriculum
- **Weekly Planning:** Structured 30-minute study sessions, 2-3 times daily

### Target Outcome
Enable a Year 5 Dulwich College student to improve performance in Math (AA group), strengthen Chinese writing skills, and maintain English proficiency through consistent, engaging, AI-guided practice.

---

## 2. Product Vision

**Vision Statement:**  
To create a personalized AI tutor that transforms daily study sessions into an engaging, rewarding journey of academic excellence, tailored specifically to one student's unique learning needs and pace.

**Problem Statement:**  
A 10-year-old student in Singapore's competitive education system struggles with advanced math concepts and Chinese writing despite being in the top-tier class group. Traditional study methods lack personalization, engagement, and adaptive difficulty, leading to frustration and inconsistent practice habits.

**Solution:**  
Kongtze provides an intelligent study companion that:
- Schedules structured weekly study sessions across all subjects
- Generates adaptive tests that match the student's current skill level
- Gamifies learning with immediate rewards and visual progress tracking
- Empowers parents with insights while keeping the student motivated
- Digitizes homework to blend school assignments with extra practice
- Learns from uploaded class notes to generate curriculum-aligned tests

---

## 3. Target Users

### 3.1 Primary User: The Student

**Profile:**
- **Name:** [Student Name]
- **Age:** 10 years old
- **Grade:** Year 5, Dulwich College Singapore
- **Academic Performance:**
  - Math: AA Class group (most advanced) - struggling with concepts
  - Chinese: Weak in writing
  - English: Average performance
  
**User Needs:**
- Fun, engaging way to practice difficult subjects
- Clear visual feedback on progress
- Rewards for consistent effort
- Age-appropriate, colorful interface
- Short, focused study sessions (30 min max)
- Immediate explanations when answers are wrong

**User Goals:**
- Improve math problem-solving speed and accuracy
- Build confidence in Chinese writing
- Maintain English proficiency
- Earn rewards and unlock gifts through learning

**Pain Points:**
- Finds advanced math frustrating without adaptive support
- Loses motivation with static, repetitive homework
- Needs immediate feedback to stay engaged
- Struggles to self-regulate study time

### 3.2 Secondary User: The Parent

**Profile:**
- **Role:** Primary decision-maker and learning supervisor
- **Tech Comfort:** Intermediate
- **Time Availability:** Busy schedule, needs efficient oversight tools

**User Needs:**
- Quick visibility into child's academic progress
- Ability to customize weekly study schedules
- Control over which subjects receive focus
- Data-driven insights on strengths/weaknesses
- Confidence that homework is being completed
- Ensure practice aligns with school curriculum

**User Goals:**
- Support child's academic success efficiently
- Identify areas needing additional focus
- Keep practice tests relevant to current classroom learning
- Balance screen time with productive learning
- Track long-term progress trends

**Pain Points:**
- Limited time to manually review all homework
- Difficulty assessing which subjects need more attention
- Wants to customize learning without being overly hands-on during sessions

---

## 4. Success Metrics

### Primary Metrics (Student Progress)
1. **Academic Performance:**
   - Test score improvement over time (per subject)
   - Math accuracy rate in AA-level problems
   - Chinese writing assessment scores
   - English proficiency maintenance

2. **Engagement Metrics:**
   - Daily session completion rate (target: >85%)
   - Average time per session (target: 25-30 min)
   - Consecutive days of practice (streak tracking)
   - Voluntary extra practice sessions initiated

3. **Learning Velocity:**
   - Time to complete questions (decreasing trend = improvement)
   - Difficulty level progression per subject
   - Questions answered correctly on first attempt

### Secondary Metrics (Platform Health)
1. **Parent Engagement:**
   - Weekly calendar customization frequency
   - Dashboard views per week
   - Parent intervention/adjustments made

2. **System Performance:**
   - AI difficulty adjustment accuracy
   - Photo-to-test conversion success rate
   - Page load time (<2 seconds)
   - Zero critical bugs affecting test-taking

---

## 5. Core Features & Requirements

### 5.1 Study Calendar Planning

**Feature Overview:**  
Weekly calendar system organizing study sessions across subjects with parent customization.

**Requirements:**
- **FR-CAL-001:** Display weekly calendar view with all scheduled sessions
- **FR-CAL-002:** Support 2-3 sessions per day, each 30 minutes
- **FR-CAL-003:** Assign different subjects to each session
- **FR-CAL-004:** Parent can modify session subjects and timings
- **FR-CAL-005:** Visual indicators for completed vs pending sessions
- **FR-CAL-006:** Auto-advance to next week on Sunday midnight
- **FR-CAL-007:** Send reminders 5 minutes before session start time

**User Stories:**
- As a parent, I want to set up a weekly schedule so my child has structured study time
- As a student, I want to see what subject I'm studying next so I can mentally prepare
- As a parent, I want to swap subjects if my child struggles in one area so the schedule adapts to needs

### 5.2 Subject Management

**Feature Overview:**  
Multi-subject support with extensible architecture for future additions.

**Requirements:**
- **FR-SUB-001:** Support Math, English, Chinese, Science as core subjects
- **FR-SUB-002:** Enable/disable subjects in parent settings
- **FR-SUB-003:** Track separate difficulty levels per subject
- **FR-SUB-004:** Maintain independent question banks per subject
- **FR-SUB-005:** Support subject-specific question types (e.g., Chinese character writing, math equations)

**User Stories:**
- As a parent, I want to focus on Math and Chinese this week so I can adjust calendar emphasis
- As a student, I want different types of questions for different subjects so practice feels varied

### 5.3 Test Generation - Homework Upload

**Feature Overview:**  
Upload photos of school homework and convert them into interactive digital tests.

**Requirements:**
- **FR-HW-001:** Accept photo uploads (JPEG, PNG, HEIC formats)
- **FR-HW-002:** Use OCR + AI to extract questions from uploaded images
- **FR-HW-003:** Present extracted questions in digital test format
- **FR-HW-004:** Allow manual correction of OCR errors by parent
- **FR-HW-005:** Assign question to appropriate subject automatically
- **FR-HW-006:** Store original photo alongside digitized questions
- **FR-HW-007:** Support multi-page homework (upload multiple images)

**User Stories:**
- As a parent, I want to upload homework photos so my child can complete them digitally
- As a student, I want to see my homework questions clearly on screen so I can answer them easily
- As a parent, I want to review extracted questions so I can fix any OCR mistakes

### 5.4 Class Notes Upload & Curriculum Tracking

**Feature Overview:**  
Upload photos of daily class notes to help AI understand current curriculum and generate contextually relevant practice tests.

**Requirements:**
- **FR-NOTES-001:** Accept class notes photo uploads (JPEG, PNG, HEIC formats)
- **FR-NOTES-002:** Use OCR + AI to extract topics, concepts, and keywords from class notes
- **FR-NOTES-003:** Automatically tag notes with subject, date, and detected topics
- **FR-NOTES-004:** Build a knowledge graph of what student is currently learning per subject
- **FR-NOTES-005:** Use class notes context when generating extra practice tests
- **FR-NOTES-006:** Display "based on recent class notes" indicator when tests use this context
- **FR-NOTES-007:** Store class notes in chronological order per subject
- **FR-NOTES-008:** Allow parent to view uploaded notes and detected topics
- **FR-NOTES-009:** AI prioritizes recent notes (last 7 days) when generating questions
- **FR-NOTES-010:** Support multi-page notes (upload multiple images per session)

**AI Integration:**
- **FR-NOTES-AI-001:** Analyze class notes to identify: key concepts, formulas, vocabulary, examples
- **FR-NOTES-AI-002:** Generate practice questions that mirror teaching style from notes
- **FR-NOTES-AI-003:** Cross-reference notes with question bank to find relevant questions
- **FR-NOTES-AI-004:** Create custom questions if no bank questions match current curriculum
- **FR-NOTES-AI-005:** Track curriculum progression over time per subject

**User Stories:**
- As a parent, I want to upload class notes daily so tests align with what my child is learning in school
- As a student, I want practice questions about what I just learned in class so it's easier to remember
- As a parent, I want to see which topics were covered in class so I know what my child is studying
- As an AI system, I want to understand the current curriculum so I generate relevant, timely practice questions

**Workflow Example:**
1. Monday: Parent uploads math class notes about "fractions addition"
2. System extracts: "adding fractions", "common denominator", "simplifying fractions"
3. Tuesday math session: AI generates test with fraction addition problems matching note examples
4. Result: Student practices exactly what was taught, reinforcing learning immediately

### 5.5 Test Generation - Extra Practice

**Feature Overview:**  
AI-generated practice tests tailored to student's current skill level.

**Requirements:**
- **FR-PRAC-001:** Generate practice tests based on subject and difficulty level
- **FR-PRAC-002:** Question count per test: 10-20 questions
- **FR-PRAC-003:** Mix of question types (multiple choice, short answer, fill-in-blank)
- **FR-PRAC-004:** Source questions from predefined question bank
- **FR-PRAC-005:** Allow parent to manually trigger extra practice session
- **FR-PRAC-006:** Auto-suggest extra practice based on weak areas

**User Stories:**
- As a student, I want extra practice in areas I'm weak so I can improve
- As a parent, I want to assign additional practice when needed so my child gets targeted help

### 5.6 AI-Powered Difficulty Adjustment

**Feature Overview:**  
Dynamic difficulty scaling based on real-time performance analysis.

**Requirements:**
- **FR-AI-001:** Track student performance per subject and topic
- **FR-AI-002:** Calculate difficulty level: Beginner, Intermediate, Advanced, Expert
- **FR-AI-003:** Adjust difficulty after every 3 tests or significant score change
- **FR-AI-004:** Increase difficulty if 3 consecutive tests score >85%
- **FR-AI-005:** Decrease difficulty if 2 consecutive tests score <50%
- **FR-AI-006:** Maintain difficulty plateau if scores are 50-85%
- **FR-AI-007:** Store difficulty adjustment history for transparency

**User Stories:**
- As a student, I want questions that match my skill level so I'm not frustrated or bored
- As a parent, I want to see how difficulty changes over time so I understand my child's progress

### 5.7 Time Limits per Question

**Feature Overview:**  
AI-generated time constraints per question based on difficulty and past performance.

**Requirements:**
- **FR-TIME-001:** Display countdown timer for each question
- **FR-TIME-002:** Calculate time limit using formula: `base_time × difficulty_multiplier × performance_factor`
- **FR-TIME-003:** Base time ranges: Easy (30s), Medium (60s), Hard (90s), Expert (120s)
- **FR-TIME-004:** Adjust time limit based on student's historical speed in that category
- **FR-TIME-005:** Visual warning when 10 seconds remaining (timer turns orange/red)
- **FR-TIME-006:** Auto-submit answer when time expires
- **FR-TIME-007:** Track time taken vs time allowed for analytics

**User Stories:**
- As a student, I want to know how much time I have so I can pace myself
- As a student, I want more time for harder questions so I don't feel rushed
- As a parent, I want to see if my child is consistently running out of time so I can identify pressure points

### 5.8 Test Results & Reporting

**Feature Overview:**  
Comprehensive post-test reports with detailed question-level breakdown.

**Requirements:**
- **FR-RESULT-001:** Display overall test score (percentage and points)
- **FR-RESULT-002:** Show per-question results: score, correct answer, student's answer, time taken
- **FR-RESULT-003:** Mark questions as correct/incorrect with visual indicators (✓/✗)
- **FR-RESULT-004:** Generate AI explanations for incorrect answers on demand
- **FR-RESULT-005:** Option to generate explanations for ALL questions (not just wrong ones)
- **FR-RESULT-006:** Store all test results in history with timestamp
- **FR-RESULT-007:** Calculate and display accuracy rate per subject over time

**User Stories:**
- As a student, I want to see which questions I got wrong so I can learn from mistakes
- As a student, I want explanations for hard questions so I understand the concepts
- As a parent, I want detailed reports so I know exactly where my child needs help

### 5.9 AI Explanations

**Feature Overview:**  
On-demand AI-generated explanations for test questions to facilitate learning.

**Requirements:**
- **FR-EXPL-001:** Generate step-by-step explanations for math problems
- **FR-EXPL-002:** Provide grammar and vocabulary explanations for English/Chinese
- **FR-EXPL-003:** Explain scientific concepts in age-appropriate language (10-year-old level)
- **FR-EXPL-004:** Include visual aids (diagrams, examples) when helpful
- **FR-EXPL-005:** Allow student to request explanation after test completion
- **FR-EXPL-006:** Store generated explanations for future reference
- **FR-EXPL-007:** Explanation language matches question language (English for English, Chinese for Chinese)

**User Stories:**
- As a student, I want simple explanations so I can understand why I was wrong
- As a student, I want to see examples so I can learn the concept better

---

## 6. Gamification System

### 6.1 Scoring System

**Requirements:**
- **FR-SCORE-001:** Assign points per question based on difficulty (Easy: 10pts, Medium: 20pts, Hard: 30pts, Expert: 50pts)
- **FR-SCORE-002:** Bonus points for fast completion (within 50% of time limit: +5pts)
- **FR-SCORE-003:** Perfect test bonus (100% accuracy: +50pts)
- **FR-SCORE-004:** Display real-time score during test
- **FR-SCORE-005:** Calculate daily total score across all sessions

### 6.2 Rewards System

**Requirements:**
- **FR-REWARD-001:** Convert test scores to reward points (1:1 ratio initially)
- **FR-REWARD-002:** Track daily, weekly, and all-time reward points
- **FR-REWARD-003:** Display reward point balance prominently in kid interface
- **FR-REWARD-004:** Celebrate milestones (100pts, 500pts, 1000pts) with animations
- **FR-REWARD-005:** Parent can manually add bonus points for offline achievements

### 6.3 Lucky Draw & Gifts

**Requirements:**
- **FR-GIFT-001:** Lucky draw available after each completed session
- **FR-GIFT-002:** Draw costs 50 reward points per spin
- **FR-GIFT-003:** Digital blind box animation with randomized rewards
- **FR-GIFT-004:** Gift types: Virtual stickers, avatar items, bonus points multipliers, study-free passes
- **FR-GIFT-005:** Parent can configure gift catalog and probabilities
- **FR-GIFT-006:** Track gift inventory in student profile
- **FR-GIFT-007:** Special rare gifts (<5% probability) for excitement

**User Stories:**
- As a student, I want to spin the lucky draw after studying so I feel rewarded
- As a student, I want to collect rare gifts so I stay motivated
- As a parent, I want to customize rewards so they align with family values

---

## 7. Parent Dashboard

**Requirements:**
- **FR-DASH-001:** Overview page showing today's completed/pending sessions
- **FR-DASH-002:** Weekly performance graph (scores over 7 days)
- **FR-DASH-003:** Subject breakdown: accuracy rate per subject
- **FR-DASH-004:** Recent test results (last 5 tests) with quick-view scores
- **FR-DASH-005:** Alerts for struggling areas (2+ consecutive low scores)
- **FR-DASH-006:** Calendar management: modify weekly schedule
- **FR-DASH-007:** Settings: enable/disable subjects, adjust session duration
- **FR-DASH-008:** Reward point balance and transaction history
- **FR-DASH-009:** Export reports as PDF for school/tutor sharing
- **FR-DASH-010:** View uploaded class notes with detected topics per subject
- **FR-DASH-011:** Upload class notes from parent dashboard

**User Stories:**
- As a parent, I want a quick daily overview so I know if my child completed studies
- As a parent, I want to spot weaknesses early so I can provide extra support
- As a parent, I want to adjust the schedule easily so it fits our family routine

---

## 8. Technical Requirements

### 8.1 Architecture Overview

**Recommended Stack:**
- **Frontend:** React.js (kid interface) + Next.js (parent dashboard)
- **Backend:** Node.js + Express.js or Python + FastAPI
- **Database:** PostgreSQL (relational data) + Redis (caching)
- **AI/ML:** OpenAI GPT-4 API (question generation, explanations, OCR enhancement)
- **Storage:** AWS S3 or similar (homework photo storage)
- **Hosting:** Vercel (frontend) + AWS/GCP (backend)

### 8.2 Data Structure (Core Entities)

**Key Database Tables:**

1. **Users**
   - `student_profile`: age, grade, school, academic_profile
   - `parent_profile`: email, notification_preferences

2. **Subjects**
   - `subject_id`, `name`, `enabled`, `difficulty_level`

3. **Calendar**
   - `weekly_schedule`: day, time, subject_id, duration
   - `session_completion`: session_id, completed_at, score

4. **Questions**
   - `question_id`, `subject_id`, `difficulty`, `type`, `content`, `correct_answer`, `explanation`
   - `source`: 'homework_upload' | 'class_notes' | 'system_generated'

4a. **Class_Notes**
   - `note_id`, `subject_id`, `uploaded_at`, `photo_url`
   - `extracted_topics[]`: list of topics/concepts detected
   - `extracted_keywords[]`: key vocabulary, formulas
   - `date_covered`: when this material was taught
   - `curriculum_context`: AI-generated summary of what's being learned

5. **Tests**
   - `test_id`, `subject_id`, `questions[]`, `created_at`, `difficulty_level`

6. **Results**
   - `test_result_id`, `test_id`, `score`, `accuracy`, `time_taken`
   - `question_results[]`: question_id, student_answer, correct, time_taken

7. **Rewards**
   - `reward_points_balance`
   - `transactions`: date, amount, source
   - `gifts_inventory`: gift_id, acquired_date

8. **Performance Analytics**
   - `subject_performance`: subject_id, accuracy_rate, difficulty_progression
   - `time_analytics`: avg_time_per_question, time_pressure_score

### 8.3 API Structure

**Backend REST API Endpoints:**

**Authentication:**
- `POST /api/auth/login` - Parent login
- `POST /api/auth/student-login` - Simple student PIN entry

**Calendar:**
- `GET /api/calendar/week` - Get current week schedule
- `PUT /api/calendar/session` - Update session subject/time
- `POST /api/calendar/session/complete` - Mark session completed

**Tests:**
- `POST /api/test/generate` - Generate new practice test
- `GET /api/test/:testId` - Retrieve test questions
- `POST /api/test/:testId/submit` - Submit test answers
- `GET /api/test/:testId/results` - Get test results

**Homework:**
- `POST /api/homework/upload` - Upload homework photo
- `GET /api/homework/:hwId/questions` - Get extracted questions
- `PUT /api/homework/:hwId/question/:qId` - Correct OCR errors

**Class Notes:**
- `POST /api/notes/upload` - Upload class notes photo
- `GET /api/notes/:noteId` - Get note details and extracted topics
- `GET /api/notes/subject/:subjectId` - Get all notes for a subject
- `GET /api/notes/recent` - Get notes from last 7 days (used for test generation)
- `PUT /api/notes/:noteId/topics` - Manually adjust detected topics

**AI Services:**
- `POST /api/ai/explain` - Generate question explanation
- `POST /api/ai/adjust-difficulty` - Trigger difficulty recalculation
- `GET /api/ai/difficulty-history` - Get difficulty adjustment log

**Rewards:**
- `GET /api/rewards/balance` - Get reward points
- `POST /api/rewards/lucky-draw` - Spin lucky draw
- `GET /api/rewards/gifts` - Get gift inventory

**Dashboard:**
- `GET /api/dashboard/overview` - Parent dashboard data
- `GET /api/dashboard/performance/:subject` - Subject-specific analytics
- `GET /api/dashboard/export` - Export PDF report

### 8.4 Non-Functional Requirements

**Performance:**
- **NFR-PERF-001:** Page load time <2 seconds on 4G connection
- **NFR-PERF-002:** Test submission response time <1 second
- **NFR-PERF-003:** AI explanation generation <5 seconds
- **NFR-PERF-004:** Homework photo OCR processing <30 seconds

**Security:**
- **NFR-SEC-001:** HTTPS encryption for all data transmission
- **NFR-SEC-002:** Student PIN (4-digit) for kid interface access
- **NFR-SEC-003:** Parent password with 2FA option
- **NFR-SEC-004:** Homework photos stored with encryption at rest

**Usability:**
- **NFR-USE-001:** Kid interface: large buttons, bright colors, minimal text
- **NFR-USE-002:** Font size: 16px minimum for readability
- **NFR-USE-003:** Mobile-responsive design (works on iPad/tablet)
- **NFR-USE-004:** Accessibility: WCAG 2.1 AA compliance

**Reliability:**
- **NFR-REL-001:** 99.5% uptime during study hours (7am-9pm SGT)
- **NFR-REL-002:** Automatic data backup daily
- **NFR-REL-003:** Graceful degradation if AI service is unavailable

**Scalability:**
- **NFR-SCALE-001:** Support 1 concurrent user initially (single student)
- **NFR-SCALE-002:** Architecture extensible to multi-user (future families)

---

## 9. User Interface Requirements

### 9.1 Kid Interface Design Principles

**Design Requirements:**
- Bright, cheerful color palette (blues, greens, yellows)
- Large, touch-friendly buttons (min 60px height)
- Playful illustrations and animations
- Minimal text, maximum visual feedback
- Progress bars and visual timers
- Celebration animations for correct answers
- Friendly error messages (no harsh red X's)

**Key Screens:**
1. **Home/Dashboard:** Today's sessions, reward points, lucky draw button
2. **Test Taking:** Question display, timer, answer input, submit button
3. **Results:** Score celebration, per-question review, explanation links
4. **Lucky Draw:** Animated blind box opening
5. **Profile:** Avatar, collected gifts, achievement badges

### 9.2 Parent Interface Design Principles

**Design Requirements:**
- Clean, professional dashboard layout
- Data visualization: charts, graphs, trend lines
- Quick-action buttons for common tasks
- Information density without clutter
- Mobile-friendly responsive design

**Key Screens:**
1. **Dashboard:** Overview, alerts, quick stats
2. **Calendar Manager:** Weekly schedule editor
3. **Performance Analytics:** Subject breakdowns, progress graphs
4. **Test History:** Searchable/filterable list of all tests
5. **Settings:** Subject management, notification preferences, reward configuration

---

## 10. Success Criteria & Acceptance

### Launch Readiness Checklist

**Must-Have for v1.0 Launch:**
- ✅ Weekly calendar with 7-day view
- ✅ At least 2 subjects fully functional (Math, Chinese)
- ✅ Homework photo upload with OCR
- ✅ Class notes upload with topic extraction
- ✅ Extra practice test generation (using class notes context)
- ✅ AI difficulty adjustment working
- ✅ Time limits per question
- ✅ Test results and scoring
- ✅ Reward points and lucky draw
- ✅ Parent dashboard with basic analytics
- ✅ Mobile-responsive kid interface

**Nice-to-Have for v1.0 (Can defer to v1.1):**
- Detailed subject-level analytics
- Advanced AI explanations with diagrams
- Gift catalog customization
- PDF report export
- Achievement badges system

### Acceptance Criteria

**Student Satisfaction:**
- Student voluntarily completes 5+ consecutive days of sessions
- Student reports finding interface "fun" or "easy to use"
- Reward redemption rate >70% (using earned points)

**Parent Satisfaction:**
- Parent can set up weekly schedule in <5 minutes
- Dashboard provides actionable insights on weak subjects
- Parent reports reduced time spent manually checking homework

**Technical Success:**
- 95%+ OCR accuracy on homework uploads
- AI difficulty adjustments result in 60-80% test scores (optimal challenge zone)
- Zero data loss incidents
- <5% bug rate in production

---

## 11. Dependencies & Constraints

### Dependencies

**External Services:**
- OpenAI API (GPT-4) for question generation and explanations
- OCR Service (Google Cloud Vision or AWS Textract) for homework photo processing
- Email/SMS service for parent notifications (optional)

**Technical Dependencies:**
- Node.js runtime environment
- PostgreSQL database
- Cloud storage (AWS S3 or equivalent)
- Hosting platform (Vercel/AWS/GCP)

### Constraints

**Single-User Focus:**
- Initial version built for one specific student
- Database schema should allow future multi-user expansion but not required for v1.0

**Singapore Education Context:**
- Question content must align with Singapore curriculum (PSLE-aligned)
- Math questions for AA group difficulty level
- Chinese questions focus on writing/composition

**Time Constraints:**
- 30-minute session maximum (attention span consideration)
- Parent availability for initial setup and weekly schedule adjustments

**Budget Constraints (Assumed):**
- Optimize AI API costs (cache frequently used explanations)
- Use cost-effective cloud hosting tier
- Consider open-source alternatives where possible

---

## 12. Risks & Mitigation

### Technical Risks

**Risk: OCR Accuracy Issues**
- **Impact:** Incorrectly digitized homework questions frustrate student
- **Mitigation:** Parent review/edit step before test activation; use best-in-class OCR service; allow manual question entry fallback

**Risk: AI Difficulty Adjustment Too Aggressive**
- **Impact:** Student discouraged by sudden difficulty spikes
- **Mitigation:** Gradual difficulty progression; parent override controls; testing with sample data before launch

**Risk: Response Time Delays (AI Generation)**
- **Impact:** Student loses focus waiting for explanations
- **Mitigation:** Loading animations; pre-generate common explanations; cache previous responses; set 5s timeout

### User Experience Risks

**Risk: Student Loses Interest After Initial Excitement**
- **Impact:** Low engagement, abandoned sessions
- **Mitigation:** Rotate reward types; introduce new gifts weekly; celebrate streaks; parent positive reinforcement integration

**Risk: Parent Overwhelmed by Dashboard Complexity**
- **Impact:** Parent disengages from monitoring
- **Mitigation:** Simple default view with "advanced" toggle; onboarding tutorial; weekly summary email

### Business/Operational Risks

**Risk: Scope Creep During Development**
- **Impact:** Delayed launch, budget overruns
- **Mitigation:** Strict MVP feature list; defer nice-to-haves to v1.1; phased rollout plan

---

## 13. Roadmap & Future Enhancements

### Phase 1: MVP (v1.0) - Target: 6-8 weeks
- Core calendar and session management
- 2 subjects (Math, Chinese)
- Homework upload + OCR
- Basic AI difficulty adjustment
- Reward points and lucky draw
- Parent dashboard basics

### Phase 2: Enhancement (v1.1) - Target: +4 weeks
- Add English and Science subjects
- Advanced analytics and reporting
- PDF export functionality
- Achievement badges system
- Voice input for answers (accessibility)

### Phase 3: Expansion (v2.0) - Target: +8 weeks
- Multi-user support (siblings/classmates)
- Social features (friendly competition, leaderboards)
- Teacher portal for homework assignment
- Mobile native apps (iOS/Android)
- Offline mode capability

### Future Considerations
- Integration with school learning management systems
- Tutoring marketplace (connect with real tutors)
- Video lesson library
- Parent community forum
- Expansion to other grade levels and curricula

---

## 14. Appendix

### Glossary

- **AA Group:** Most advanced math class grouping at Dulwich College
- **Blind Box:** Mystery reward container with randomized contents
- **Difficulty Adjustment:** AI process of changing question difficulty based on performance
- **Greenfield Project:** New product built from scratch (no existing codebase)
- **Lucky Draw:** Gamified reward mechanism using virtual spinning/drawing
- **OCR:** Optical Character Recognition (converting images to text)
- **Session:** 30-minute study period focused on one subject

### References

- Singapore Primary School Leaving Examination (PSLE) syllabus
- Dulwich College Singapore curriculum guidelines
- WCAG 2.1 Accessibility Guidelines
- Child online safety best practices (COPPA, GDPR considerations)

---

**END OF PRD**

---

## Document Status

- ✅ Executive Summary Complete
- ✅ Product Vision Defined
- ✅ Target Users Profiled
- ✅ Success Metrics Established
- ✅ Core Features Specified
- ✅ Gamification System Detailed
- ✅ Technical Architecture Outlined
- ✅ UI/UX Requirements Defined
- ✅ Dependencies & Risks Identified
- ✅ Roadmap Planned

**Next Steps:**
1. Review and approve this PRD
2. Create Architecture Document (technical design)
3. Break down into Epics & User Stories
4. Begin Sprint Planning for Phase 1 (MVP)