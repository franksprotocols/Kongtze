---
title: 'Test Generation with Multiple Input Sources'
slug: 'test-generation-multi-source'
created: '2026-01-27'
status: 'completed'
stepsCompleted: [1, 2, 3]
tech_stack: ['Next.js 15', 'React 19', 'TypeScript', 'FastAPI', 'SQLAlchemy 2.0', 'Gemini AI']
files_to_modify: [
  'kongtze-backend/app/schemas/test.py',
  'kongtze-backend/app/models/test.py',
  'kongtze-backend/app/api/tests.py',
  'kongtze-backend/app/services/ai_service.py',
  'kongtze-frontend/app/dashboard/subjects/[id]/page.tsx',
  'kongtze-frontend/app/dashboard/calendar/generate/page.tsx',
  'kongtze-frontend/lib/types.ts'
]
code_patterns: []
test_patterns: []
---

# Tech-Spec: Test Generation with Multiple Input Sources

**Created:** 2026-01-27

## Overview

### Problem Statement

Currently, users can only generate tests through the manual test creation flow at `/dashboard/tests/new`. There's no way to automatically generate tests when creating study schedules, and no way to generate tests based on uploaded class notes or homework. This limits the platform's ability to create curriculum-aligned, contextually relevant practice tests that match what the student is currently learning in school.

### Solution

Add three new test generation entry points with multiple input source options:

1. **Schedule Integration**: Add optional checkbox in AI schedule generator (`/dashboard/calendar/generate`) to auto-create tests for scheduled study sessions
2. **Subject Detail Page**: Create new `/dashboard/subjects/[id]` page with comprehensive test generation UI
3. **Three Generation Modes**:
   - Pure AI (existing functionality)
   - Notes-based (select specific uploaded class notes)
   - Homework-based (select specific uploaded homework)

### Scope

**In Scope:**
- Add "Generate tests for sessions" checkbox to schedule generation flow (step 2 of wizard)
- Create new `/dashboard/subjects/[id]` page with test generation options
- Extend `POST /api/tests` endpoint to accept optional `note_ids[]` and `homework_ids[]` parameters
- Update AI service to incorporate notes/homework context when generating questions
- UI for selecting specific notes/homework from a list with preview
- Difficulty level (1-4) and question count (5-20) selection for all modes
- Display which notes/homework were used in test metadata

**Out of Scope:**
- Automatic test generation without user action
- Editing existing tests after creation
- Bulk test generation across multiple subjects simultaneously
- Test scheduling/reminders
- Merging questions from multiple sources in a single test

## Context for Development

### Codebase Patterns

**Frontend (Next.js 15 + React 19):**
- App Router with file-based routing in `app/` directory
- TanStack Query v5 for server state management
- TypeScript strict mode with explicit types
- Tailwind CSS 4 for styling (no inline styles)
- Co-located components with routes

**Backend (FastAPI + SQLAlchemy 2.0):**
- Async/await for all database operations
- Pydantic V2 for request/response validation
- SQLAlchemy 2.0 syntax with `Mapped[T]` and `mapped_column`
- Dependency injection for database sessions
- JWT authentication with bearer tokens

**AI Integration:**
- Gemini API via REST (httpx AsyncClient)
- Prompt engineering for test generation
- JSON response parsing with fallback handling

### Files to Reference

| File | Purpose |
| ---- | ------- |
| `kongtze-backend/app/api/tests.py` | Existing test creation endpoint |
| `kongtze-backend/app/services/ai_service.py` | AI service with test generation |
| `kongtze-frontend/app/dashboard/calendar/generate/page.tsx` | Schedule generation wizard |
| `kongtze-backend/app/api/class_notes.py` | Class notes API |
| `kongtze-backend/app/api/homework.py` | Homework API |
| `_bmad-output/project-context.md` | Project patterns and conventions |

### Technical Decisions

**Context Passing to AI Service:**
- Extend `ai_service.generate_test_questions()` to accept optional `context_text: Optional[str]` parameter
- Backend fetches full OCR text from database based on provided note_ids/homework_ids
- AI prompt will be modified to include: "Generate questions based on this content: {context_text}"
- Context text will be truncated to 4000 characters max to avoid token limits

**API Parameter Design:**
- Frontend passes `note_ids: List[int]` and/or `homework_ids: List[int]` in TestCreate schema
- Backend queries ClassNote and Homework tables to fetch OCR text
- Concatenate all OCR texts with separators: "--- Note 1 ---\n{text}\n--- Note 2 ---\n{text}"
- Pass concatenated text as context_text to AI service

**Subject Detail Page Structure:**
```
/dashboard/subjects/[id]
├── Header: Subject name, description
├── Generation Mode Selector (3 buttons/tabs)
│   ├── Pure AI (default, existing flow)
│   ├── Based on Notes (shows note selection UI)
│   └── Based on Homework (shows homework selection UI)
├── Common Controls (all modes)
│   ├── Difficulty Level: 1-4 slider
│   ├── Question Count: 5-20 slider
│   └── Generate Test button
└── Mode-Specific UI
    ├── Notes Mode: List of notes with checkboxes + preview
    └── Homework Mode: List of homework with checkboxes + preview
```

**Test Metadata Storage:**
- Add optional fields to Test model:
  - `source_note_ids: Optional[List[int]]` (JSON field)
  - `source_homework_ids: Optional[List[int]]` (JSON field)
  - `generation_mode: str` (enum: "pure_ai", "notes_based", "homework_based")
- Display source materials in test detail view

**Schedule Integration Flow:**
1. Add checkbox in step 2: "Generate practice tests for scheduled subjects"
2. Store checkbox state in component state
3. After schedule is accepted and sessions are created:
   - If checkbox is checked, extract unique subject_ids from schedule
   - For each subject, call `POST /api/tests` with:
     - subject_id
     - title: "Practice Test for {subject_name}"
     - difficulty_level: 2 (Intermediate)
     - total_questions: 10
     - generation_mode: "pure_ai"
4. Show success message: "Schedule created with {n} practice tests"

## Implementation Plan

### Tasks

#### Phase 1: Backend - Extend Test API

**Task 1.1: Update Test Model**
- Add `source_note_ids` field (JSON, nullable)
- Add `source_homework_ids` field (JSON, nullable)
- Add `generation_mode` field (String, default="pure_ai")
- Create database migration

**Task 1.2: Update Test Schemas**
- Extend `TestCreate` schema to accept optional `note_ids: List[int]` and `homework_ids: List[int]`
- Update `TestResponse` schema to include new metadata fields
- Add validation: at least one of note_ids or homework_ids required if mode is not "pure_ai"

**Task 1.3: Extend AI Service**
- Add `context_text: Optional[str]` parameter to `generate_test_questions()`
- Modify prompt to include context when provided
- Add context truncation logic (max 4000 chars)
- Test with sample context text

**Task 1.4: Update Test Creation Endpoint**
- Fetch ClassNote records if note_ids provided
- Fetch Homework records if homework_ids provided
- Verify all notes/homework belong to current user (403 if not)
- Concatenate OCR texts with separators
- Pass context to AI service
- Store source IDs and generation mode in test record

#### Phase 2: Frontend - Subject Detail Page

**Task 2.1: Create Subject Detail Page**
- Create `/dashboard/subjects/[id]/page.tsx`
- Fetch subject details and verify it exists
- Create page layout with header

**Task 2.2: Build Generation Mode Selector**
- Create three mode buttons: Pure AI, Notes, Homework
- Implement mode state management
- Style active/inactive states

**Task 2.3: Build Common Controls**
- Difficulty level slider (1-4) with labels
- Question count slider (5-20)
- Generate Test button with loading state

**Task 2.4: Build Notes Selection UI**
- Fetch notes for current subject
- Display list with checkboxes
- Show note title, date, preview of OCR text
- Track selected note IDs in state

**Task 2.5: Build Homework Selection UI**
- Fetch homework for current subject
- Display list with checkboxes
- Show homework title, date, preview of OCR text
- Track selected homework IDs in state

**Task 2.6: Implement Test Generation**
- Call `POST /api/tests` with appropriate parameters based on mode
- Handle loading and error states
- Redirect to test page on success
- Show error message on failure

#### Phase 3: Frontend - Schedule Integration

**Task 3.1: Add Checkbox to Schedule Wizard**
- Add checkbox in step 2: "Generate practice tests for scheduled subjects"
- Store checkbox state in preferences
- Style checkbox consistently with existing UI

**Task 3.2: Implement Post-Schedule Test Creation**
- After schedule acceptance, check if checkbox was checked
- Extract unique subject_ids from generated schedule
- Create tests for each subject in parallel
- Show success message with count of tests created
- Handle partial failures gracefully

#### Phase 4: Frontend - Type Definitions

**Task 4.1: Update TypeScript Types**
- Add `source_note_ids`, `source_homework_ids`, `generation_mode` to Test type
- Add `note_ids`, `homework_ids` to TestCreate type
- Export new types

#### Phase 5: Testing & Polish

**Task 5.1: Backend Testing**
- Test all new API parameters
- Test authorization (notes/homework ownership)
- Test AI service with context

**Task 5.2: Frontend Testing**
- Test subject detail page flows
- Test schedule integration
- Test error handling

**Task 5.3: UI Polish**
- Ensure consistent styling
- Add loading states
- Add helpful error messages
- Test responsive design

### Acceptance Criteria

**Schedule Integration:**
- [x] Checkbox appears in step 2 of schedule generation wizard
- [ ] Checkbox is optional (unchecked by default)
- [ ] When checked and schedule is accepted, tests are created for each unique subject
- [ ] Success message shows number of tests created
- [ ] Tests have title "Practice Test for {Subject}"
- [ ] Tests use difficulty level 2 and 10 questions

**Subject Detail Page:**
- [ ] Page accessible at `/dashboard/subjects/[id]`
- [ ] Shows subject name and description
- [ ] Three generation modes are clearly presented
- [ ] Pure AI mode works like existing test creation
- [ ] Notes mode shows list of available notes for that subject
- [ ] Homework mode shows list of available homework for that subject
- [ ] User can select multiple notes/homework with checkboxes
- [ ] Difficulty level selector (1-4) works in all modes
- [ ] Question count selector (5-20) works in all modes
- [ ] Generate button creates test and redirects to test page

**API Functionality:**
- [ ] `POST /api/tests` accepts optional `note_ids` array
- [ ] `POST /api/tests` accepts optional `homework_ids` array
- [ ] API fetches OCR text from selected notes/homework
- [ ] API passes context to AI service
- [ ] Generated questions are contextually relevant to provided materials
- [ ] Test metadata stores source note/homework IDs
- [ ] Test metadata stores generation mode
- [ ] API returns 403 if user tries to use notes/homework they don't own
- [ ] API returns 404 if note/homework IDs don't exist

**Test Display:**
- [ ] Test detail page shows which notes/homework were used (if any)
- [ ] Test list shows generation mode indicator
- [ ] Tests created from schedule are clearly labeled

**Error Handling:**
- [ ] Appropriate error messages for invalid note/homework IDs
- [ ] Appropriate error messages for authorization failures
- [ ] Graceful fallback if AI service fails
- [ ] Loading states during test generation
- [ ] Validation prevents generating test without selecting notes/homework in those modes

## Additional Context

### Dependencies

- Existing `POST /api/tests` endpoint
- Existing `ai_service.generate_test_questions()` method
- Class notes and homework upload functionality
- Schedule generation workflow

### Testing Strategy

**Backend Testing:**
- Test `POST /api/tests` with note_ids parameter
- Test `POST /api/tests` with homework_ids parameter
- Test `POST /api/tests` with both note_ids and homework_ids
- Verify OCR text is correctly fetched and passed to AI service
- Test with invalid note/homework IDs (should return 404)
- Test with notes/homework belonging to different user (should return 403)

**Frontend Testing:**
- Test subject detail page renders correctly
- Test mode switching between Pure AI, Notes, Homework
- Test note/homework selection UI
- Test schedule generation with checkbox checked/unchecked
- Verify tests are created after schedule acceptance
- Test difficulty and question count controls

**Integration Testing:**
- End-to-end: Upload note → Generate test from note → Verify questions are contextual
- End-to-end: Create schedule with checkbox → Verify tests are created
- Verify test metadata correctly stores source note/homework IDs

### Notes

- User wants optional checkbox (not automatic) for schedule integration
- User wants to select specific notes/homework (not automatic "use all recent")
- Three distinct generation modes should be clearly presented in UI
- All modes should support difficulty and question count selection
