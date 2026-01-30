/**
 * TypeScript types for Kongtze API
 * These match the Pydantic schemas from the backend
 */

// User types
export interface User {
  user_id: number;
  name: string;
  email?: string;
  is_parent: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserCreateParent {
  name: string;
  email: string;
  password: string;
}

export interface UserCreateStudent {
  name: string;
  pin: string;
}

export interface UserLogin {
  email?: string;
  pin?: string;
  password?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// Subject types
export interface Subject {
  subject_id: number;
  name: string;
  display_name: string;
  description?: string;
}

// Study Session types
export interface StudySession {
  session_id: number;
  user_id: number;
  subject_id: number;
  day_of_week: number; // 0=Monday, 6=Sunday
  start_time: string; // HH:MM:SS
  duration_minutes: number;
  difficulty_level?: number; // 1=beginner, 2=intermediate, 3=advanced, 4=expert
  title?: string;
  created_at: string;
  updated_at: string;
}

export interface StudySessionCreate {
  subject_id: number;
  day_of_week: number;
  start_time: string;
  duration_minutes?: number;
  difficulty_level?: number;
  title?: string;
}

export interface StudySessionUpdate {
  subject_id?: number;
  day_of_week?: number;
  start_time?: string;
  duration_minutes?: number;
  difficulty_level?: number;
  title?: string;
}

// Test types
export interface Question {
  question_id: number;
  test_id: number;
  question_text: string;
  options: Record<string, string>; // { A: "...", B: "...", C: "...", D: "..." }
  time_limit_seconds: number;
  created_at: string;
}

export interface QuestionWithAnswer extends Question {
  correct_answer: string;
}

export interface Test {
  test_id: number;
  user_id: number;
  subject_id: number;
  title: string;
  difficulty_level: number; // 1-4
  time_limit_minutes: number;
  total_questions: number;
  source_note_ids?: number[];
  source_homework_ids?: number[];
  generation_mode: string; // "pure_ai" | "notes_based" | "homework_based"
  created_at: string;
}

export interface TestWithQuestions extends Test {
  questions: Question[];
}

export interface TestCreate {
  subject_id: number;
  title: string;
  difficulty_level: number;
  time_limit_minutes?: number;
  total_questions?: number;
  note_ids?: number[];
  homework_ids?: number[];
  generation_mode?: string; // "pure_ai" | "notes_based" | "homework_based"
}

export interface TestSubmission {
  test_id: number;
  answers: Record<string, string>; // { question_id: "A" }
  time_taken_seconds: number;
}

export interface TestResult {
  result_id: number;
  test_id: number;
  user_id: number;
  score: number;
  total_score: number;
  time_taken_seconds: number;
  answers: Record<string, string>;
  reward_points: number;
  completed_at: string;
}

export interface TestResultWithReview extends TestResult {
  questions: QuestionWithAnswer[];
  percentage: number;
}

// Homework types
export interface Homework {
  homework_id: number;
  user_id: number;
  subject_id: number;
  title: string;
  photo_path: string;
  ocr_text?: string;
  parent_reviewed: boolean;
  created_at: string;
  updated_at: string;
}

export interface HomeworkUpdate {
  title?: string;
  parent_reviewed?: boolean;
}

// Class Note types
export interface Topic {
  topic_id: number;
  note_id: number;
  subject_id: number;
  topic_name: string;
  confidence: number;
  extracted_at: string;
}

export interface ClassNote {
  note_id: number;
  user_id: number;
  subject_id: number;
  title: string;
  photo_path: string;
  ocr_text?: string;
  created_at: string;
}

export interface ClassNoteWithTopics extends ClassNote {
  topics: Topic[];
}

export interface ClassNoteUpdate {
  title?: string;
}

// Reward types
export interface Reward {
  reward_id: number;
  user_id: number;
  points: number;
  reason: string;
  balance: number;
  created_at: string;
}

export interface RewardBalance {
  balance: number;
  total_earned: number;
}

// Gift types
export interface Gift {
  gift_id: number;
  name: string;
  description?: string;
  tier: 'gold' | 'silver' | 'bronze';
  probability: number;
  image_path?: string;
  created_at: string;
}

export interface GiftCreate {
  name: string;
  description?: string;
  tier: 'gold' | 'silver' | 'bronze';
  probability: number;
  image_path?: string;
}

export interface LuckyDrawResult {
  gift: Gift;
  points_spent: number;
  remaining_balance: number;
}
