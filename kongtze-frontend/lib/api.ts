/**
 * API service functions for Kongtze frontend
 */

import { apiClient } from './api-client';
import type {
  User,
  UserCreateParent,
  UserCreateStudent,
  UserLogin,
  Token,
  Subject,
  StudySession,
  StudySessionCreate,
  StudySessionUpdate,
  Test,
  TestWithQuestions,
  TestCreate,
  TestSubmission,
  TestResult,
  TestResultWithReview,
  Homework,
  HomeworkUpdate,
  ClassNote,
  ClassNoteWithTopics,
  ClassNoteUpdate,
  Reward,
  RewardBalance,
  Gift,
  GiftCreate,
  LuckyDrawResult,
} from './types';

// Auth API
export const authAPI = {
  registerParent: (data: UserCreateParent) =>
    apiClient.post<Token>('/auth/register/parent', data),

  registerStudent: (data: UserCreateStudent, token: string) =>
    apiClient.post<User>('/auth/register/student', data, token),

  login: (credentials: UserLogin) =>
    apiClient.post<Token>('/auth/login', credentials),

  getCurrentUser: (token: string) =>
    apiClient.get<User>('/auth/me', token),
};

// Subjects API
export const subjectsAPI = {
  getAll: (token: string) =>
    apiClient.get<Subject[]>('/subjects', token),

  getById: (id: number, token: string) =>
    apiClient.get<Subject>(`/subjects/${id}`, token),
};

// Study Sessions API
export const studySessionsAPI = {
  getAll: (token: string) =>
    apiClient.get<StudySession[]>('/study-sessions', token),

  getById: (id: number, token: string) =>
    apiClient.get<StudySession>(`/study-sessions/${id}`, token),

  create: (data: StudySessionCreate, token: string) =>
    apiClient.post<StudySession>('/study-sessions', data, token),

  update: (id: number, data: StudySessionUpdate, token: string) =>
    apiClient.put<StudySession>(`/study-sessions/${id}`, data, token),

  delete: (id: number, token: string) =>
    apiClient.delete(`/study-sessions/${id}`, token),
};

// Tests API
export const testsAPI = {
  create: (data: TestCreate, token: string) =>
    apiClient.post<TestWithQuestions>('/tests', data, token),

  getAll: (token: string, subjectId?: number) => {
    const params = subjectId ? `?subject_id=${subjectId}` : '';
    return apiClient.get<Test[]>(`/tests${params}`, token);
  },

  getById: (id: number, token: string) =>
    apiClient.get<TestWithQuestions>(`/tests/${id}`, token),

  submit: (submission: TestSubmission, token: string) =>
    apiClient.post<TestResult>('/tests/submit', submission, token),

  getResult: (resultId: number, token: string) =>
    apiClient.get<TestResultWithReview>(`/tests/results/${resultId}`, token),

  getAllResults: (token: string) =>
    apiClient.get<TestResult[]>('/tests/results', token),
};

// Homework API
export const homeworkAPI = {
  upload: (subjectId: number, title: string, photo: File, token: string) => {
    const formData = new FormData();
    formData.append('subject_id', subjectId.toString());
    formData.append('title', title);
    formData.append('photo', photo);

    return apiClient.upload<Homework>('/homework', formData, token);
  },

  getAll: (token: string, subjectId?: number, reviewed?: boolean) => {
    const params = new URLSearchParams();
    if (subjectId) params.append('subject_id', subjectId.toString());
    if (reviewed !== undefined) params.append('reviewed', reviewed.toString());

    const query = params.toString() ? `?${params.toString()}` : '';
    return apiClient.get<Homework[]>(`/homework${query}`, token);
  },

  getById: (id: number, token: string) =>
    apiClient.get<Homework>(`/homework/${id}`, token),

  update: (id: number, data: HomeworkUpdate, token: string) =>
    apiClient.put<Homework>(`/homework/${id}`, data, token),

  delete: (id: number, token: string) =>
    apiClient.delete(`/homework/${id}`, token),
};

// Class Notes API
export const classNotesAPI = {
  upload: (subjectId: number, title: string, photo: File, token: string) => {
    const formData = new FormData();
    formData.append('subject_id', subjectId.toString());
    formData.append('title', title);
    formData.append('photo', photo);

    return apiClient.upload<ClassNoteWithTopics>('/class-notes', formData, token);
  },

  getAll: (token: string, subjectId?: number) => {
    const params = subjectId ? `?subject_id=${subjectId}` : '';
    return apiClient.get<ClassNote[]>(`/class-notes${params}`, token);
  },

  getById: (id: number, token: string) =>
    apiClient.get<ClassNoteWithTopics>(`/class-notes/${id}`, token),

  update: (id: number, data: ClassNoteUpdate, token: string) =>
    apiClient.put<ClassNote>(`/class-notes/${id}`, data, token),

  delete: (id: number, token: string) =>
    apiClient.delete(`/class-notes/${id}`, token),
};

// Rewards API
export const rewardsAPI = {
  getBalance: (token: string) =>
    apiClient.get<RewardBalance>('/rewards/balance', token),

  getHistory: (token: string, limit: number = 50) =>
    apiClient.get<Reward[]>(`/rewards/history?limit=${limit}`, token),

  // Gifts
  getAllGifts: (token: string, tier?: string) => {
    const params = tier ? `?tier=${tier}` : '';
    return apiClient.get<Gift[]>(`/rewards/gifts${params}`, token);
  },

  createGift: (data: GiftCreate, token: string) =>
    apiClient.post<Gift>('/rewards/gifts', data, token),

  deleteGift: (id: number, token: string) =>
    apiClient.delete(`/rewards/gifts/${id}`, token),

  // Lucky draw
  luckyDraw: (token: string) =>
    apiClient.post<LuckyDrawResult>('/rewards/lucky-draw', {}, token),
};
