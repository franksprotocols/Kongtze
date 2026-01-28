/**
 * Tests List Page
 * View all generated tests and their results
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { testsAPI, subjectsAPI } from '@/lib/api';
import Link from 'next/link';

export default function TestsPage() {
  const { token } = useAuth();

  const { data: tests = [], isLoading } = useQuery({
    queryKey: ['tests'],
    queryFn: () => testsAPI.getAll(token!),
    enabled: !!token,
  });

  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectsAPI.getAll(token!),
    enabled: !!token,
  });

  const getSubjectName = (subjectId: number) => {
    return subjects.find((s) => s.subject_id === subjectId)?.display_name || 'Unknown';
  };

  const getDifficultyLabel = (level: number) => {
    const labels = ['', 'Beginner', 'Intermediate', 'Advanced', 'Expert'];
    return labels[level] || 'Unknown';
  };

  const getDifficultyColor = (level: number) => {
    const colors = [
      '',
      'bg-green-100 text-green-800',
      'bg-blue-100 text-blue-800',
      'bg-orange-100 text-orange-800',
      'bg-red-100 text-red-800',
    ];
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Tests</h1>
          <p className="text-gray-600 mt-1">View and take your AI-generated tests</p>
        </div>
        <Link
          href="/dashboard/tests/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
        >
          + Generate New Test
        </Link>
      </div>

      {/* Tests List */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tests...</p>
        </div>
      ) : tests.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm p-12 border text-center">
          <svg
            className="w-16 h-16 text-gray-300 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No tests yet</h3>
          <p className="text-gray-600 mb-6">Generate your first AI-powered test to get started</p>
          <Link
            href="/dashboard/tests/new"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Generate Test
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {tests.map((test) => (
            <div
              key={test.test_id}
              className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{test.title}</h3>
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(
                        test.difficulty_level
                      )}`}
                    >
                      {getDifficultyLabel(test.difficulty_level)}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                        />
                      </svg>
                      {getSubjectName(test.subject_id)}
                    </span>
                    <span className="flex items-center gap-1">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                        />
                      </svg>
                      {test.total_questions} questions
                    </span>
                    <span className="flex items-center gap-1">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      {test.time_limit_minutes} min
                    </span>
                  </div>

                  <p className="text-xs text-gray-500 mt-2">
                    Created {new Date(test.created_at).toLocaleDateString()}
                  </p>
                </div>

                <Link
                  href={`/dashboard/tests/${test.test_id}/take`}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm"
                >
                  Start Test
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
