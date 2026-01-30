/**
 * Study Sessions Calendar Page
 * Weekly schedule view with CRUD operations
 */

'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { studySessionsAPI, subjectsAPI } from '@/lib/api';
import type { StudySession, StudySessionCreate, Subject } from '@/lib/types';
import Link from 'next/link';

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const TIME_SLOTS = Array.from({ length: 14 }, (_, i) => {
  const hour = i + 8; // Start from 8 AM
  return `${hour.toString().padStart(2, '0')}:00`;
});

const SUBJECT_COLORS: Record<string, string> = {
  math: 'bg-blue-100 text-blue-800 border-blue-300',
  english: 'bg-green-100 text-green-800 border-green-300',
  chinese: 'bg-red-100 text-red-800 border-red-300',
  science: 'bg-purple-100 text-purple-800 border-purple-300',
};

export default function CalendarPage() {
  const { token } = useAuth();
  const queryClient = useQueryClient();
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSession, setSelectedSession] = useState<StudySession | null>(null);

  // Fetch sessions and subjects
  const { data: sessions = [] } = useQuery({
    queryKey: ['study-sessions'],
    queryFn: () => studySessionsAPI.getAll(token!),
    enabled: !!token,
  });

  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectsAPI.getAll(token!),
    enabled: !!token,
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => studySessionsAPI.delete(id, token!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['study-sessions'] });
    },
  });

  // Clear all sessions mutation
  const clearAllMutation = useMutation({
    mutationFn: async () => {
      await studySessionsAPI.deleteAll(token!);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['study-sessions'] });
      alert('Calendar cleared successfully!');
    },
    onError: (error) => {
      console.error('Failed to clear calendar:', error);
      alert('Failed to clear calendar. Please try again.');
    },
  });

  const getSessionsForSlot = (dayIndex: number, timeSlot: string) => {
    return sessions.filter((session) => {
      const sessionHour = session.start_time.split(':')[0];
      const slotHour = timeSlot.split(':')[0];
      return session.day_of_week === dayIndex && sessionHour === slotHour;
    });
  };

  const getSubjectById = (subjectId: number) => {
    return subjects.find((s) => s.subject_id === subjectId);
  };

  const handleDeleteSession = (id: number) => {
    if (confirm('Are you sure you want to delete this study session?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleClearCalendar = () => {
    if (confirm('Are you sure you want to clear ALL study sessions? This cannot be undone.')) {
      clearAllMutation.mutate();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Study Calendar</h1>
          <p className="text-gray-600 mt-1">Manage your weekly study schedule</p>
        </div>
        <div className="flex gap-3">
          <Link
            href="/dashboard/calendar/generate"
            className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 font-medium"
          >
            ✨ AI Generate Schedule
          </Link>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            + Add Study Session
          </button>
          <button
            onClick={handleClearCalendar}
            disabled={clearAllMutation.isPending || sessions.length === 0}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {clearAllMutation.isPending ? 'Clearing...' : '🗑️ Clear Calendar'}
          </button>
        </div>
      </div>

      {/* Legend */}
      <div className="bg-white rounded-lg shadow-sm p-4 border">
        <p className="text-sm font-medium text-gray-700 mb-2">Subjects:</p>
        <div className="flex gap-4">
          {subjects.map((subject) => (
            <div key={subject.subject_id} className="flex items-center gap-2">
              <div
                className={`w-4 h-4 rounded ${
                  SUBJECT_COLORS[subject.name] || 'bg-gray-100'
                }`}
              />
              <span className="text-sm text-gray-700">{subject.display_name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border p-3 text-left text-sm font-medium text-gray-700 w-24">
                  Time
                </th>
                {DAYS.map((day) => (
                  <th
                    key={day}
                    className="border p-3 text-center text-sm font-medium text-gray-700"
                  >
                    {day}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {TIME_SLOTS.map((timeSlot) => (
                <tr key={timeSlot}>
                  <td className="border p-3 text-sm text-gray-600 font-medium bg-gray-50">
                    {timeSlot}
                  </td>
                  {DAYS.map((_, dayIndex) => {
                    const slotSessions = getSessionsForSlot(dayIndex, timeSlot);

                    return (
                      <td key={dayIndex} className="border p-2 align-top h-24">
                        <div className="space-y-1">
                          {slotSessions.map((session) => {
                            const subject = getSubjectById(session.subject_id);
                            return (
                              <div
                                key={session.session_id}
                                className={`p-2 rounded border text-xs ${
                                  SUBJECT_COLORS[subject?.name || ''] ||
                                  'bg-gray-100 text-gray-800 border-gray-300'
                                }`}
                              >
                                <div className="flex items-start justify-between gap-1">
                                  <div className="flex-1 min-w-0">
                                    <p className="font-semibold truncate">
                                      {subject?.display_name}
                                    </p>
                                    <p className="text-xs opacity-75">
                                      {session.start_time.slice(0, 5)} ({session.duration_minutes}
                                      min)
                                    </p>
                                    {session.difficulty_level && (
                                      <p className="text-xs opacity-75 mt-0.5">
                                        Level: {['', 'Beginner', 'Intermediate', 'Advanced', 'Expert'][session.difficulty_level]}
                                      </p>
                                    )}
                                    {session.title && (
                                      <p className="text-xs truncate mt-1">{session.title}</p>
                                    )}
                                  </div>
                                  <button
                                    onClick={() => handleDeleteSession(session.session_id)}
                                    className="opacity-50 hover:opacity-100"
                                  >
                                    <svg
                                      className="w-3 h-3"
                                      fill="none"
                                      stroke="currentColor"
                                      viewBox="0 0 24 24"
                                    >
                                      <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M6 18L18 6M6 6l12 12"
                                      />
                                    </svg>
                                  </button>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Session Modal */}
      {showAddModal && (
        <AddSessionModal
          subjects={subjects}
          onClose={() => setShowAddModal(false)}
          onSuccess={() => {
            setShowAddModal(false);
            queryClient.invalidateQueries({ queryKey: ['study-sessions'] });
          }}
        />
      )}
    </div>
  );
}

// Add Session Modal Component
function AddSessionModal({
  subjects,
  onClose,
  onSuccess,
}: {
  subjects: Subject[];
  onClose: () => void;
  onSuccess: () => void;
}) {
  const { token } = useAuth();
  const [formData, setFormData] = useState({
    subject_id: subjects[0]?.subject_id || 1,
    day_of_week: 0,
    start_time: '09:00',
    duration_minutes: 30,
    title: '',
  });

  const createMutation = useMutation({
    mutationFn: (data: StudySessionCreate) => studySessionsAPI.create(data, token!),
    onSuccess,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate({
      ...formData,
      start_time: `${formData.start_time}:00`,
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Add Study Session</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
            <select
              value={formData.subject_id}
              onChange={(e) =>
                setFormData({ ...formData, subject_id: parseInt(e.target.value) })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {subjects.map((subject) => (
                <option key={subject.subject_id} value={subject.subject_id}>
                  {subject.display_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Day</label>
            <select
              value={formData.day_of_week}
              onChange={(e) =>
                setFormData({ ...formData, day_of_week: parseInt(e.target.value) })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {DAYS.map((day, index) => (
                <option key={day} value={index}>
                  {day}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Start Time</label>
            <input
              type="time"
              value={formData.start_time}
              onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Duration (minutes)
            </label>
            <select
              value={formData.duration_minutes}
              onChange={(e) =>
                setFormData({ ...formData, duration_minutes: parseInt(e.target.value) })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value={15}>15 minutes</option>
              <option value={30}>30 minutes</option>
              <option value={45}>45 minutes</option>
              <option value={60}>60 minutes</option>
              <option value={90}>90 minutes</option>
              <option value={120}>120 minutes</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title (Optional)
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Algebra practice"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={createMutation.isPending}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {createMutation.isPending ? 'Adding...' : 'Add Session'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
