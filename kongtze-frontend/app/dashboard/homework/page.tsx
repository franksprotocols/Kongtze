/**
 * Homework List Page
 * View all uploaded homework with OCR text
 */

'use client';

import { useState, Component, ErrorInfo, ReactNode } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { homeworkAPI, subjectsAPI, studySessionsAPI } from '@/lib/api';
import Link from 'next/link';
import type { Homework, StudySession } from '@/lib/types';

// Error Boundary for Modal
class ModalErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(_: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Modal error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
            <h2 className="text-xl font-bold text-red-600 mb-4">Something went wrong</h2>
            <p className="text-gray-600 mb-4">
              An error occurred while loading the schedule modal. Please try again.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default function HomeworkPage() {
  const { token, user } = useAuth();
  const queryClient = useQueryClient();

  // State for modal
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [selectedHomework, setSelectedHomework] = useState<Homework | null>(null);

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

  // Fetch study sessions for modal
  const { data: studySessions = [] } = useQuery({
    queryKey: ['study-sessions'],
    queryFn: () => studySessionsAPI.getAll(token!),
    enabled: !!token && showScheduleModal,
  });

  // Mutation for updating session
  const updateSessionMutation = useMutation({
    mutationFn: async ({ sessionId, homeworkData }: { sessionId: number; homeworkData: Homework }) => {
      return studySessionsAPI.update(
        sessionId,
        {
          subject_id: homeworkData.subject_id,
          title: `Homework: ${homeworkData.title}`,
        },
        token!
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['study-sessions'] });
      setShowScheduleModal(false);
      setSelectedHomework(null);
      alert('Homework scheduled successfully!');
    },
    onError: (error) => {
      console.error('Failed to schedule homework:', error);
      alert('Failed to schedule homework. Please try again.');
    },
  });

  const handleSetDate = (hw: Homework) => {
    setSelectedHomework(hw);
    setShowScheduleModal(true);
  };

  const handleSessionSelect = (session: StudySession) => {
    if (selectedHomework) {
      const sessionSubject = getSubjectName(session.subject_id);
      const confirmMessage = `Replace "${sessionSubject}" session on ${DAYS[session.day_of_week]} at ${session.start_time.substring(0, 5)} with homework "${selectedHomework.title}"?`;

      if (window.confirm(confirmMessage)) {
        updateSessionMutation.mutate({
          sessionId: session.session_id,
          homeworkData: selectedHomework,
        });
      }
    }
  };

  const getSubjectName = (subjectId: number) => {
    return subjects.find((s) => s.subject_id === subjectId)?.display_name || 'Unknown';
  };

  const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

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

                <div className="flex flex-col gap-2 ml-4">
                  <button
                    onClick={() => handleSetDate(hw)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm whitespace-nowrap"
                  >
                    📅 Set Date
                  </button>
                  {user?.is_parent && !hw.parent_reviewed && (
                    <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium text-sm whitespace-nowrap">
                      Mark Reviewed
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Schedule Modal */}
      {showScheduleModal && (
        <ModalErrorBoundary>
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-3xl w-full max-h-[80vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="p-6 border-b">
              <h2 className="text-2xl font-bold text-gray-900">Schedule Homework</h2>
              <p className="text-gray-600 mt-1">
                Select a session to replace with: <span className="font-semibold">{selectedHomework?.title}</span>
              </p>
            </div>

            {/* Modal Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {studySessions.length === 0 ? (
                <div className="text-center py-12">
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
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">No sessions available</h3>
                  <p className="text-gray-600 mb-6">Generate a schedule first to assign homework to sessions</p>
                  <Link
                    href="/dashboard/calendar/generate"
                    className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
                  >
                    Generate Schedule
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {DAYS.map((day, dayIndex) => {
                    const daySessions = studySessions.filter((s) => s.day_of_week === dayIndex);

                    if (daySessions.length === 0) return null;

                    return (
                      <div key={day} className="border rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-3">{day}</h3>
                        <div className="space-y-2">
                          {daySessions.map((session) => (
                            <button
                              key={session.session_id}
                              onClick={() => handleSessionSelect(session)}
                              disabled={updateSessionMutation.isPending}
                              className="w-full flex items-center justify-between bg-gray-50 hover:bg-blue-50 rounded-lg p-3 transition-colors border border-gray-200 hover:border-blue-300 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              <div className="text-left">
                                <p className="font-medium text-gray-900">
                                  {getSubjectName(session.subject_id)}
                                </p>
                                <p className="text-sm text-gray-600">
                                  {session.start_time.substring(0, 5)} ({session.duration_minutes} min)
                                </p>
                                {session.title && (
                                  <p className="text-xs text-gray-500 mt-1">{session.title}</p>
                                )}
                              </div>
                              <svg
                                className="w-5 h-5 text-gray-400"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M9 5l7 7-7 7"
                                />
                              </svg>
                            </button>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-6 border-t">
              <button
                onClick={() => {
                  setShowScheduleModal(false);
                  setSelectedHomework(null);
                }}
                disabled={updateSessionMutation.isPending}
                className="w-full px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          </div>
          </div>
        </ModalErrorBoundary>
      )}
    </div>
  );
}
