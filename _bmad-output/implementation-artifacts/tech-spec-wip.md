---
title: 'Schedule Generation & Homework Scheduling Improvements'
slug: 'schedule-homework-improvements'
created: '2026-01-28'
status: 'completed'
stepsCompleted: [1, 2, 3, 4, 5, 6]
tech_stack: ['Next.js 15', 'React 19', 'TypeScript', 'FastAPI', 'SQLAlchemy 2.0', 'Gemini AI', 'TanStack Query v5', 'Tailwind CSS 4']
files_to_modify: [
  'kongtze-backend/app/api/study_sessions.py',
  'kongtze-frontend/app/dashboard/homework/page.tsx',
  'kongtze-frontend/lib/types.ts'
]
code_patterns: [
  'Async/await for all database operations',
  'TanStack Query for server state management',
  'Client components with "use client" directive',
  'Tailwind CSS utility classes for styling',
  'Modal/dialog pattern for interactive UI'
]
test_patterns: []
---

# Tech-Spec: Schedule Generation & Homework Scheduling Improvements

**Created:** 2026-01-28

## Overview

### Problem Statement

The current AI schedule generation system has several limitations that reduce its effectiveness:

1. **Session Duration Issues**: Sessions can be 60-90 minutes, which is too long for effective study/testing sessions
2. **Incorrect Dinner Time**: The dinner time constraint is set to 19:00-19:30, but should be 19:00-19:40
3. **No Daily Session Limits**: There's no constraint on the maximum number of sessions per day, which could lead to overwhelming schedules
4. **Repeated Subjects**: The same subject can be scheduled multiple times in one day, which isn't optimal for learning
5. **No Manual Homework Scheduling**: When parents/students upload school homework, there's no way to manually assign it to a specific calendar slot

These limitations result in schedules that may not be practical or effective for students.

### Solution

Implement two complementary improvements:

**Part 1: AI Schedule Generation Constraints**
- Limit session durations to 30 or 45 minutes only (remove 60 and 90 minute options)
- Update dinner time constraint to 19:00-19:40 (7:00 PM - 7:40 PM)
- Enforce maximum 3 sessions per day
- Prevent the same subject from appearing twice in one day

**Part 2: Manual Homework Scheduling**
- Add "Set Date" button on homework list page
- Allow users to select an existing calendar session
- Replace the selected session with a homework-based test session
- Maintain all time constraints when scheduling

### Scope

**In Scope:**
- Modify AI prompt in `/study-sessions/generate-schedule` endpoint to enforce new constraints
- Change session duration options from [30, 45, 60, 90] to [30, 45] minutes
- Update dinner time constraint from 19:00-19:30 to 19:00-19:40
- Add constraint: maximum 3 sessions per day
- Add constraint: no repeated subjects within the same day
- Add "Set Date" button to homework list page
- Create session picker UI showing existing calendar sessions
- Implement session replacement logic for homework-based tests
- Respect all time constraints (user's time window, dinner time, 45-min max duration)

**Out of Scope:**
- Creating new calendar sessions (only replacing existing ones)
- Automatic homework scheduling without user action
- Modifying database schema or data models
- Bulk homework scheduling operations
- Changing the test generation logic itself
- Adding validation after schedule generation (constraints enforced in AI prompt)

## Context for Development

### Codebase Patterns

**Backend (FastAPI + SQLAlchemy 2.0):**
- Async/await for all database operations
- Pydantic V2 for request/response validation
- SQLAlchemy 2.0 syntax with `Mapped[T]` and `mapped_column`
- JWT authentication with bearer tokens
- AI service uses Gemini API via REST (httpx AsyncClient)

**Frontend (Next.js 15 + React 19):**
- App Router with file-based routing
- TanStack Query v5 for server state management
- TypeScript strict mode with explicit types
- Tailwind CSS 4 for styling
- Client components for interactive features

**Key Patterns Found:**
- Schedule generation uses AI prompt engineering at `/study-sessions/generate-schedule`
- Current prompt includes dinner time constraint (19:00-19:30) and session durations [30, 45, 60, 90]
- Homework list page exists at `/dashboard/homework`
- Study sessions are stored in `study_sessions` table with fields: subject_id, day_of_week, start_time, duration_minutes

### Files to Reference

| File | Purpose |
| ---- | ------- |
| `kongtze-backend/app/api/study_sessions.py` | Contains `/generate-schedule` endpoint with AI prompt |
| `kongtze-frontend/app/dashboard/homework/page.tsx` | Homework list page where "Set Date" button will be added |
| `kongtze-frontend/app/dashboard/calendar/page.tsx` | Calendar view showing study sessions |
| `kongtze-backend/app/models/study_session.py` | StudySession model definition |
| `kongtze-backend/app/schemas/study_session.py` | StudySession schemas for API |
| `_bmad-output/project-context.md` | Project patterns and conventions |

### Technical Decisions

**AI Prompt Modifications:**
- Update the prompt constraints section to include all four new rules
- Change session duration list from [30, 45, 60, 90] to [30, 45]
- Update dinner time from "19:00-19:30" to "19:00-19:40"
- Add explicit instruction: "Maximum 3 sessions per day"
- Add explicit instruction: "Each subject can only appear once per day"

**Homework Scheduling Approach:**
- Add "Set Date" button to each homework item in the list
- When clicked, open a modal/dialog showing the user's weekly calendar
- Display existing sessions grouped by day with subject, time, and duration
- Allow user to click on a session to replace it
- Update the selected session's subject_id to match the homework's subject
- Optionally update the session title to indicate it's homework-based

**Session Replacement Logic:**
- Fetch user's existing study sessions
- Display them in a selectable format
- On selection, call `PUT /study-sessions/{session_id}` to update the session
- Update subject_id and optionally title to reflect homework assignment

## Implementation Plan

### Tasks

#### Phase 1: Backend - AI Schedule Generation Improvements

**Task 1.1: Update AI Prompt Constraints** ✓
- File: `kongtze-backend/app/api/study_sessions.py`
- Action: Modified the AI prompt in `/generate-schedule` endpoint (lines 246-280)
  - Changed session duration list from `[30, 45, 60, 90]` to `[30, 45]` (line 256)
  - Updated dinner time from "19:00-19:30" to "19:00-19:40" (line 255)
  - Added constraint: "Maximum 3 sessions per day" in IMPORTANT CONSTRAINTS section
  - Added constraint: "Each subject can only appear once per day" in IMPORTANT CONSTRAINTS section
- Notes: Kept existing constraint structure, just updated values and added new rules

**Task 1.2: Add Post-Generation Validation (Optional but Recommended)** ✓
- File: `kongtze-backend/app/api/study_sessions.py`
- Action: Added validation function after AI response parsing (after line 295)
  - Validates max 3 sessions per day
  - Validates no repeated subjects per day
  - Validates session durations are only 30 or 45 minutes
  - Validates no sessions during 19:00-19:40
  - Returns error if validation fails
- Notes: This addresses the concern raised by Murat (Test Architect) about AI non-determinism

#### Phase 2: Frontend - Homework Scheduling Feature

**Task 2.1: Add Session Picker Modal Component** ✓
- File: `kongtze-frontend/app/dashboard/homework/page.tsx`
- Action: Created a modal component that displays user's weekly calendar
  - Fetches study sessions using `studySessionsAPI.getAll()`
  - Groups sessions by day of week
  - Displays each session with: day, time, subject, duration
  - Makes sessions clickable for selection
  - Added "Cancel" button to close modal
- Notes: Used Tailwind CSS for styling, followed existing modal patterns in codebase

**Task 2.2: Add "Set Date" Button to Homework Items** ✓
- File: `kongtze-frontend/app/dashboard/homework/page.tsx`
- Action: Added button to each homework card (around line 142)
  - Button text: "📅 Set Date"
  - On click: opens session picker modal with homework context
  - Passes homework_id and subject_id to modal
- Notes: Placed button next to "Mark Reviewed" button

**Task 2.3: Implement Session Replacement Logic** ✓
- File: `kongtze-frontend/app/dashboard/homework/page.tsx`
- Action: Added mutation to update selected session
  - Uses `studySessionsAPI.update(session_id, { subject_id, title }, token)`
  - Updates session's subject_id to match homework's subject_id
  - Updates session's title to "Homework: {homework.title}"
  - Shows success message after update
  - Invalidates queries to refresh calendar
- Notes: Used TanStack Query's `useMutation` hook

**Task 2.4: Add State Management for Modal** ✓
- File: `kongtze-frontend/app/dashboard/homework/page.tsx`
- Action: Added React state for modal visibility and selected homework
  - `const [showScheduleModal, setShowScheduleModal] = useState(false)`
  - `const [selectedHomework, setSelectedHomework] = useState<Homework | null>(null)`
  - Passed state to modal component
- Notes: Followed existing state management patterns in the file

### Acceptance Criteria

#### AI Schedule Generation Improvements

- [ ] **AC 1.1**: Given a user generates a schedule, when the AI creates sessions, then all sessions have duration of either 30 or 45 minutes (no 60 or 90 minute sessions)

- [ ] **AC 1.2**: Given a user generates a schedule, when the AI creates sessions, then no sessions are scheduled between 19:00-19:40 (dinner time)

- [ ] **AC 1.3**: Given a user generates a schedule, when the AI creates sessions, then no day has more than 3 sessions

- [ ] **AC 1.4**: Given a user generates a schedule, when the AI creates sessions, then no subject appears more than once on the same day

- [ ] **AC 1.5**: Given the AI generates an invalid schedule (violates constraints), when validation runs, then an error is returned and the user is prompted to regenerate

#### Homework Scheduling Feature

- [ ] **AC 2.1**: Given a user views the homework list page, when they see a homework item, then a "Set Date" button is visible on each homework card

- [ ] **AC 2.2**: Given a user clicks "Set Date" on a homework item, when the modal opens, then they see their weekly calendar with all existing study sessions grouped by day

- [ ] **AC 2.3**: Given a user views sessions in the modal, when they see each session, then it displays: day name, start time, subject name, and duration

- [ ] **AC 2.4**: Given a user selects a session in the modal, when they click on it, then the session is updated to use the homework's subject and title is set to "Homework: {title}"

- [ ] **AC 2.5**: Given a user successfully schedules homework, when the update completes, then a success message is shown and the modal closes

- [ ] **AC 2.6**: Given a user schedules homework to a session, when they view the calendar, then the updated session shows the homework title

- [ ] **AC 2.7**: Given a user clicks "Cancel" in the modal, when the modal closes, then no changes are made to any sessions

#### Error Handling

- [ ] **AC 3.1**: Given the API returns an error during session update, when the error occurs, then an error message is displayed to the user

- [ ] **AC 3.2**: Given a user has no existing sessions, when they click "Set Date", then the modal shows a message "No sessions available. Generate a schedule first."

## Additional Context

### Dependencies

- Existing `/study-sessions/generate-schedule` endpoint
- Existing homework upload and list functionality
- Existing calendar/schedule display
- AI service (Gemini) for schedule generation

### Testing Strategy

**Backend Testing:**
- Test `/generate-schedule` endpoint with various preferences
- Verify AI prompt includes all four new constraints
- Test validation function with invalid schedules:
  - Schedule with 4 sessions in one day (should fail)
  - Schedule with same subject twice in one day (should fail)
  - Schedule with 60-minute session (should fail)
  - Schedule with session during 19:00-19:40 (should fail)
- Test `PUT /study-sessions/{session_id}` endpoint for session updates

**Frontend Testing:**
- Test "Set Date" button appears on homework items
- Test modal opens and displays sessions correctly
- Test session selection and update flow
- Test success/error message display
- Test modal close behavior (Cancel button)
- Test with empty sessions list (no sessions available)

**Integration Testing:**
- End-to-end: Generate schedule → Verify all constraints met
- End-to-end: Upload homework → Set date → Verify session updated on calendar
- Verify calendar reflects homework-based sessions correctly

**Manual Testing:**
- Generate multiple schedules and verify consistency
- Test homework scheduling with different subjects
- Verify UI responsiveness and user experience

### Notes

- User clarified that "study sessions" are actually "testing sessions" - students take tests (either homework-based or AI-generated)
- The constraint "no repeated subjects per day" applies to testing sessions
- Manual homework scheduling only replaces existing sessions, doesn't create new ones
- All time constraints (user's time window, dinner time, max duration) must be respected

## Review Notes

**Adversarial Review Completed:** 2026-01-28

**Findings:** 20 total findings identified
- 5 HIGH severity
- 7 MEDIUM severity
- 8 LOW severity

**Resolution Approach:** Auto-fix (HIGH severity issues)

**Fixes Applied:**
- F1: Added error handling for malformed time strings in validation (try-catch, format validation)
- F4: Added confirmation dialog before session replacement (window.confirm with context)
- F10: Added error boundary wrapping modal (ModalErrorBoundary component)

**Deferred:**
- F14: Unit tests - requires test infrastructure setup
- F15: Integration tests - requires E2E test setup

**Skipped:** 15 MEDIUM/LOW severity findings (can be addressed in future iterations)
