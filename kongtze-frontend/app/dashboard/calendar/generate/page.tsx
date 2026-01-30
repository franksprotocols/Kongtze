/**
 * AI Study Schedule Generator
 * Generate optimized weekly study schedule using AI
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { subjectsAPI, studySessionsAPI, testsAPI } from '@/lib/api';
import { apiClient } from '@/lib/api-client';

interface SchedulePreferences {
  subjects: number[];
  subjectDifficulties: Record<number, string>; // subject_id -> difficulty level
  hoursPerDay: number;
  startTime: string;
  endTime: string;
  goals: string;
  generateTests: boolean; // New field for test generation
}

export default function GenerateSchedulePage() {
  const router = useRouter();
  const { token } = useAuth();
  const [step, setStep] = useState(1);
  const [preferences, setPreferences] = useState<SchedulePreferences>({
    subjects: [],
    subjectDifficulties: {},
    hoursPerDay: 2,
    startTime: '14:00',
    endTime: '20:00',
    goals: '',
    generateTests: false,
  });
  const [generatedSchedule, setGeneratedSchedule] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectsAPI.getAll(token!),
    enabled: !!token,
  });

  const handleSubjectToggle = (subjectId: number) => {
    setPreferences((prev) => {
      const isRemoving = prev.subjects.includes(subjectId);
      const newSubjects = isRemoving
        ? prev.subjects.filter((id) => id !== subjectId)
        : [...prev.subjects, subjectId];

      // Remove difficulty if subject is removed
      const newDifficulties = { ...prev.subjectDifficulties };
      if (isRemoving) {
        delete newDifficulties[subjectId];
      } else {
        // Set default difficulty for new subject
        newDifficulties[subjectId] = 'intermediate';
      }

      return {
        ...prev,
        subjects: newSubjects,
        subjectDifficulties: newDifficulties,
      };
    });
  };

  const handleDifficultyChange = (subjectId: number, difficulty: string) => {
    setPreferences((prev) => ({
      ...prev,
      subjectDifficulties: {
        ...prev.subjectDifficulties,
        [subjectId]: difficulty,
      },
    }));
  };

  const generateSchedule = async () => {
    setIsGenerating(true);
    try {
      // Call AI service to generate schedule
      const response = await apiClient.post<any>(
        '/study-sessions/generate-schedule',
        preferences,
        token!
      );
      setGeneratedSchedule(response.schedule);
      setStep(3);
    } catch (error) {
      console.error('Failed to generate schedule:', error);
      alert('Failed to generate schedule. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const createSessionsMutation = useMutation({
    mutationFn: async () => {
      // Map difficulty text to numeric level
      const difficultyMap: Record<string, number> = {
        'beginner': 1,
        'intermediate': 2,
        'advanced': 3,
      };

      // Create all sessions from generated schedule
      const sessionPromises = generatedSchedule.map((session) => {
        const difficultyText = preferences.subjectDifficulties[session.subject_id] || 'intermediate';
        const difficultyLevel = difficultyMap[difficultyText] || 2;

        return studySessionsAPI.create(
          {
            subject_id: session.subject_id,
            day_of_week: session.day_of_week,
            start_time: session.start_time,
            duration_minutes: session.duration_minutes,
            difficulty_level: difficultyLevel,
          },
          token!
        );
      });
      await Promise.all(sessionPromises);

      // Create tests if checkbox is checked
      if (preferences.generateTests) {
        // Get unique subject IDs from schedule
        const uniqueSubjectIds = [...new Set(generatedSchedule.map((s) => s.subject_id))];

        // Map difficulty text to numeric level
        const difficultyMap: Record<string, number> = {
          'beginner': 1,
          'intermediate': 2,
          'advanced': 3,
        };

        // Create a test for each subject using their selected difficulty
        const testPromises = uniqueSubjectIds.map((subjectId) => {
          const subject = subjects.find((s) => s.subject_id === subjectId);
          const difficultyText = preferences.subjectDifficulties[subjectId] || 'intermediate';
          const difficultyLevel = difficultyMap[difficultyText] || 2;

          return testsAPI.create(
            {
              subject_id: subjectId,
              title: `Practice Test for ${subject?.display_name || 'Subject'}`,
              difficulty_level: difficultyLevel,
              time_limit_minutes: 30,
              total_questions: 10,
              generation_mode: 'pure_ai',
            },
            token!
          );
        });

        await Promise.all(testPromises);
        return { testsCreated: uniqueSubjectIds.length };
      }

      return { testsCreated: 0 };
    },
    onSuccess: (data) => {
      if (data.testsCreated > 0) {
        alert(`Schedule created with ${data.testsCreated} practice tests!`);
      }
      router.push('/dashboard/calendar');
    },
    onError: (error) => {
      console.error('Failed to create schedule:', error);
      alert('Failed to create schedule. Please try again.');
    },
  });

  const handleAcceptSchedule = () => {
    createSessionsMutation.mutate();
  };

  const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AI Study Schedule Generator</h1>
        <p className="text-gray-600 mt-2">
          Let AI create an optimized weekly study schedule for you
        </p>
      </div>

      {/* Step 1: Subject Selection */}
      {step === 1 && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Step 1: Select Subjects & Difficulty
            </h2>
            <p className="text-gray-600 mb-4">
              Choose subjects and set difficulty level for each
            </p>

            <div className="space-y-3">
              {subjects.map((subject) => {
                const isSelected = preferences.subjects.includes(subject.subject_id);
                return (
                  <div
                    key={subject.subject_id}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <button
                        onClick={() => handleSubjectToggle(subject.subject_id)}
                        className="flex items-center gap-3 flex-1"
                      >
                        <div
                          className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                            isSelected
                              ? 'border-blue-500 bg-blue-500'
                              : 'border-gray-300'
                          }`}
                        >
                          {isSelected && (
                            <svg
                              className="w-4 h-4 text-white"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clipRule="evenodd"
                              />
                            </svg>
                          )}
                        </div>
                        <span className="font-medium text-gray-900">{subject.display_name}</span>
                      </button>

                      {isSelected && (
                        <select
                          value={preferences.subjectDifficulties[subject.subject_id] || 'intermediate'}
                          onChange={(e) => handleDifficultyChange(subject.subject_id, e.target.value)}
                          onClick={(e) => e.stopPropagation()}
                          className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="beginner">Beginner (P1-2)</option>
                          <option value="intermediate">Intermediate (P3-4)</option>
                          <option value="advanced">Advanced (P5-6)</option>
                        </select>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="flex justify-end">
            <button
              onClick={() => setStep(2)}
              disabled={preferences.subjects.length === 0}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next: Set Preferences
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Preferences */}
      {step === 2 && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border space-y-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Step 2: Set Your Preferences
            </h2>

            {/* Hours per day */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-3">
                Study Hours Per Day
              </label>
              <input
                type="range"
                min="1"
                max="12"
                step="0.5"
                value={preferences.hoursPerDay}
                onChange={(e) =>
                  setPreferences({ ...preferences, hoursPerDay: parseFloat(e.target.value) })
                }
                className="w-full"
              />
              <div className="flex justify-between text-sm text-gray-600 mt-2">
                <span>1 hour</span>
                <span className="font-semibold text-blue-600">
                  {preferences.hoursPerDay} {preferences.hoursPerDay === 1 ? 'hour' : 'hours'}
                </span>
                <span>6 hours</span>
              </div>
            </div>

            {/* Time range */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Preferred Start Time
                </label>
                <input
                  type="time"
                  value={preferences.startTime}
                  onChange={(e) =>
                    setPreferences({ ...preferences, startTime: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Preferred End Time
                </label>
                <input
                  type="time"
                  value={preferences.endTime}
                  onChange={(e) =>
                    setPreferences({ ...preferences, endTime: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Goals */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-3">
                Study Goals (Optional)
              </label>
              <textarea
                value={preferences.goals}
                onChange={(e) => setPreferences({ ...preferences, goals: e.target.value })}
                placeholder="e.g., Prepare for upcoming exams, improve weak areas, maintain good grades..."
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Generate Tests Checkbox */}
            <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <input
                type="checkbox"
                id="generateTests"
                checked={preferences.generateTests}
                onChange={(e) => setPreferences({ ...preferences, generateTests: e.target.checked })}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500 mt-0.5"
              />
              <div className="flex-1">
                <label htmlFor="generateTests" className="block text-sm font-semibold text-gray-900 cursor-pointer">
                  Generate practice tests for scheduled subjects
                </label>
                <p className="text-sm text-gray-600 mt-1">
                  Automatically create a practice test for each subject using the difficulty level you selected above
                </p>
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => setStep(1)}
              className="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50"
            >
              Back
            </button>
            <button
              onClick={generateSchedule}
              disabled={isGenerating}
              className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              {isGenerating ? (
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
                  Generating with AI...
                </span>
              ) : (
                '✨ Generate Schedule'
              )}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Preview & Accept */}
      {step === 3 && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Step 3: Review Your Schedule
            </h2>
            <p className="text-gray-600 mb-6">
              AI has generated an optimized study schedule for you. Review and accept to add it to
              your calendar.
            </p>

            <div className="space-y-4">
              {DAYS.map((day, dayIndex) => {
                const daySessions = generatedSchedule.filter(
                  (s) => s.day_of_week === dayIndex
                );

                return (
                  <div key={day} className="border rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 mb-3">{day}</h3>
                    {daySessions.length === 0 ? (
                      <p className="text-sm text-gray-500">Rest day</p>
                    ) : (
                      <div className="space-y-2">
                        {daySessions.map((session, idx) => {
                          const subject = subjects.find(
                            (s) => s.subject_id === session.subject_id
                          );
                          return (
                            <div
                              key={idx}
                              className="flex items-center justify-between bg-blue-50 rounded p-3"
                            >
                              <div>
                                <p className="font-medium text-gray-900">
                                  {subject?.display_name}
                                </p>
                                <p className="text-sm text-gray-600">
                                  {session.start_time} ({session.duration_minutes} min)
                                </p>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => setStep(2)}
              className="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50"
            >
              Regenerate
            </button>
            <button
              onClick={handleAcceptSchedule}
              disabled={createSessionsMutation.isPending}
              className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:opacity-50"
            >
              {createSessionsMutation.isPending ? 'Adding to Calendar...' : '✓ Accept Schedule'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

