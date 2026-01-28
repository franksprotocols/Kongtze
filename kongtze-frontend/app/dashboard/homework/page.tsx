/**
 * Homework List Page
 * View all uploaded homework with OCR text
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { homeworkAPI, subjectsAPI } from '@/lib/api';
import Link from 'next/link';

export default function HomeworkPage() {
  const { token, user } = useAuth();

  const { data: homework = [], isLoading } = useQuery({
    queryKey: ['homework'],
    queryFn: () => homeworkAPI.getAll(token!),
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Homework</h1>
          <p className="text-gray-600 mt-1">Upload and review homework with AI OCR</p>
        </div>
        <Link
          href="/dashboard/homework/upload"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
        >
          + Upload Homework
        </Link>
      </div>

      {/* Homework List */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading homework...</p>
        </div>
      ) : homework.length === 0 ? (
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
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No homework yet</h3>
          <p className="text-gray-600 mb-6">Upload your first homework photo to get started</p>
          <Link
            href="/dashboard/homework/upload"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Upload Homework
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {homework.map((hw) => (
            <div
              key={hw.homework_id}
              className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{hw.title}</h3>
                    {hw.parent_reviewed && (
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                        ✓ Reviewed
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
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
                      {getSubjectName(hw.subject_id)}
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
                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                      </svg>
                      {new Date(hw.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  {/* OCR Text Preview */}
                  {hw.ocr_text && (
                    <div className="bg-gray-50 rounded-lg p-4 border">
                      <p className="text-xs font-medium text-gray-700 mb-2">
                        📝 Extracted Text (OCR):
                      </p>
                      <p className="text-sm text-gray-600 line-clamp-3">{hw.ocr_text}</p>
                    </div>
                  )}
                </div>

                {user?.is_parent && !hw.parent_reviewed && (
                  <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium text-sm ml-4">
                    Mark Reviewed
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
