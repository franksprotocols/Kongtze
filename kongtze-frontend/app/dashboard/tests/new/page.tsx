/**
 * Test Generation Page
 * AI-powered test creation wizard
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { testsAPI, subjectsAPI } from '@/lib/api';
import type { TestCreate } from '@/lib/types';

const DIFFICULTY_LEVELS = [
  { value: 0, label: 'Auto (Recommended)', description: 'AI adapts based on your performance', color: 'bg-purple-100 text-purple-800' },
  { value: 1, label: 'Beginner', description: 'Primary 1-2 level', color: 'bg-green-100 text-green-800' },
  { value: 2, label: 'Intermediate', description: 'Primary 3-4 level', color: 'bg-blue-100 text-blue-800' },
  { value: 3, label: 'Advanced', description: 'Primary 5-6 level', color: 'bg-orange-100 text-orange-800' },
  { value: 4, label: 'Expert', description: 'PSLE preparation', color: 'bg-red-100 text-red-800' },
];

export default function NewTestPage() {
  const router = useRouter();
  const { token } = useAuth();
  const [formData, setFormData] = useState<TestCreate>({
    subject_id: 1,
    title: '',
    difficulty_level: 0,
    time_limit_minutes: 30,
    total_questions: 0,
  });

  // Fetch subjects
  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectsAPI.getAll(token!),
    enabled: !!token,
  });

  // Generate test mutation
  const generateMutation = useMutation({
    mutationFn: (data: TestCreate) => testsAPI.create(data, token!),
    onSuccess: (data) => {
      router.push(`/dashboard/tests/${data.test_id}/take`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    generateMutation.mutate(formData);
  };

  const selectedSubject = subjects.find((s) => s.subject_id === formData.subject_id);

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Generate New Test</h1>
        <p className="text-gray-600 mt-2">
          AI will create personalized questions based on your preferences
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Subject Selection */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Select Subject
          </label>
          <div className="grid grid-cols-2 gap-3">
            {subjects.map((subject) => (
              <button
                key={subject.subject_id}
                type="button"
                onClick={() => setFormData({ ...formData, subject_id: subject.subject_id })}
                className={`p-4 rounded-lg border-2 transition-all ${
                  formData.subject_id === subject.subject_id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <p className="font-semibold text-gray-900">{subject.display_name}</p>
                {subject.description && (
                  <p className="text-xs text-gray-500 mt-1">{subject.description}</p>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Test Title */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Test Title
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            placeholder={`${selectedSubject?.display_name || 'Subject'} Practice Test`}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        {/* Difficulty Level */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Difficulty Level
          </label>
          <div className="grid grid-cols-2 gap-3">
            {DIFFICULTY_LEVELS.map((level) => (
              <button
                key={level.value}
                type="button"
                onClick={() => setFormData({ ...formData, difficulty_level: level.value })}
                className={`p-4 rounded-lg border-2 transition-all ${
                  formData.difficulty_level === level.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-gray-900">{level.label}</span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${level.color}`}>
                    Level {level.value}
                  </span>
                </div>
                <p className="text-xs text-gray-500 text-left">{level.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Number of Questions */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Number of Questions
          </label>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setFormData({ ...formData, total_questions: 0 })}
                className={`flex-1 p-3 rounded-lg border-2 transition-all ${
                  formData.total_questions === 0
                    ? 'border-purple-500 bg-purple-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-gray-900">Auto (Recommended)</span>
                  <span className="px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-800">
                    AI Decides
                  </span>
                </div>
                <p className="text-xs text-gray-500 text-left mt-1">
                  AI calculates optimal question count based on session length
                </p>
              </button>
              <button
                type="button"
                onClick={() => setFormData({ ...formData, total_questions: 10 })}
                className={`flex-1 p-3 rounded-lg border-2 transition-all ${
                  formData.total_questions > 0
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-gray-900">Manual</span>
                  <span className="px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    Custom
                  </span>
                </div>
                <p className="text-xs text-gray-500 text-left mt-1">
                  Choose specific number of questions
                </p>
              </button>
            </div>
            {formData.total_questions > 0 && (
              <div>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="5"
                    max="20"
                    step="5"
                    value={formData.total_questions}
                    onChange={(e) =>
                      setFormData({ ...formData, total_questions: parseInt(e.target.value) })
                    }
                    className="flex-1"
                  />
                  <span className="text-2xl font-bold text-blue-600 w-12 text-right">
                    {formData.total_questions}
                  </span>
                </div>
                <div className="flex justify-between text-xs text-gray-500 mt-2">
                  <span>5 questions</span>
                  <span>20 questions</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Time Limit */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Time Limit (minutes)
          </label>
          <select
            value={formData.time_limit_minutes}
            onChange={(e) =>
              setFormData({ ...formData, time_limit_minutes: parseInt(e.target.value) })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={15}>15 minutes</option>
            <option value={20}>20 minutes</option>
            <option value={30}>30 minutes</option>
            <option value={45}>45 minutes</option>
            <option value={60}>60 minutes</option>
          </select>
        </div>

        {/* Submit Button */}
        <div className="flex gap-3">
          <button
            type="button"
            onClick={() => router.back()}
            className="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={generateMutation.isPending}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generateMutation.isPending ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Generating Test with AI...
              </span>
            ) : (
              '✨ Generate Test with AI'
            )}
          </button>
        </div>
      </form>

      {/* Error Display */}
      {generateMutation.isError && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <p className="font-medium">Failed to generate test</p>
          <p className="text-sm mt-1">
            {(generateMutation.error as any)?.detail || 'Please try again'}
          </p>
        </div>
      )}
    </div>
  );
}
