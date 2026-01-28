/**
 * Subject Detail Page with Test Generation
 * Allows generating tests with three modes: Pure AI, Notes-based, Homework-based
 */

'use client';

import { useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { subjectsAPI, testsAPI, classNotesAPI, homeworkAPI } from '@/lib/api';

type GenerationMode = 'pure_ai' | 'notes_based' | 'homework_based';

export default function SubjectDetailPage() {
  const router = useRouter();
  const params = useParams();
  const { token } = useAuth();
  const subjectId = parseInt(params.id as string);

  const [mode, setMode] = useState<GenerationMode>('pure_ai');
  const [difficultyLevel, setDifficultyLevel] = useState(2);
  const [questionCount, setQuestionCount] = useState(10);
  const [selectedNoteIds, setSelectedNoteIds] = useState<number[]>([]);
  const [selectedHomeworkIds, setSelectedHomeworkIds] = useState<number[]>([]);

  // Fetch subject details
  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectsAPI.getAll(token!),
    enabled: !!token,
  });

  const subject = subjects.find((s) => s.subject_id === subjectId);

  // Fetch notes for this subject
  const { data: notes = [] } = useQuery({
    queryKey: ['class-notes', subjectId],
    queryFn: () => classNotesAPI.getAll(token!, subjectId),
    enabled: !!token && mode === 'notes_based',
  });

  // Fetch homework for this subject
  const { data: homework = [] } = useQuery({
    queryKey: ['homework', subjectId],
    queryFn: () => homeworkAPI.getAll(token!, subjectId),
    enabled: !!token && mode === 'homework_based',
  });

  // Create test mutation
  const createTestMutation = useMutation({
    mutationFn: async () => {
      const testData: any = {
        subject_id: subjectId,
        title: `${subject?.display_name} Practice Test`,
        difficulty_level: difficultyLevel,
        time_limit_minutes: 30,
        total_questions: questionCount,
        generation_mode: mode,
      };

      if (mode === 'notes_based' && selectedNoteIds.length > 0) {
        testData.note_ids = selectedNoteIds;
      }

      if (mode === 'homework_based' && selectedHomeworkIds.length > 0) {
        testData.homework_ids = selectedHomeworkIds;
      }

      return testsAPI.create(testData, token!);
    },
    onSuccess: (data) => {
      router.push(`/dashboard/tests/${data.test_id}`);
    },
  });

  const handleGenerateTest = () => {
    // Validation
    if (mode === 'notes_based' && selectedNoteIds.length === 0) {
      alert('Please select at least one note');
      return;
    }

    if (mode === 'homework_based' && selectedHomeworkIds.length === 0) {
      alert('Please select at least one homework');
      return;
    }

    createTestMutation.mutate();
  };

  const handleNoteToggle = (noteId: number) => {
    setSelectedNoteIds((prev) =>
      prev.includes(noteId) ? prev.filter((id) => id !== noteId) : [...prev, noteId]
    );
  };

  const handleHomeworkToggle = (homeworkId: number) => {
    setSelectedHomeworkIds((prev) =>
      prev.includes(homeworkId) ? prev.filter((id) => id !== homeworkId) : [...prev, homeworkId]
    );
  };

  if (!subject) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-600">Subject not found</p>
      </div>
    );
  }

  const difficultyLabels = ['Beginner', 'Intermediate', 'Advanced', 'Expert'];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{subject.display_name}</h1>
        <p className="text-gray-600 mt-2">Generate practice tests for this subject</p>
      </div>

      {/* Generation Mode Selector */}
      <div className="bg-white rounded-xl shadow-sm p-6 border">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Generation Mode</h2>
        <div className="flex gap-3">
          <button
            onClick={() => setMode('pure_ai')}
            className={`flex-1 px-4 py-3 rounded-lg font-medium transition-all ${
              mode === 'pure_ai'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Pure AI
          </button>
          <button
            onClick={() => setMode('notes_based')}
            className={`flex-1 px-4 py-3 rounded-lg font-medium transition-all ${
              mode === 'notes_based'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Based on Notes
          </button>
          <button
            onClick={() => setMode('homework_based')}
            className={`flex-1 px-4 py-3 rounded-lg font-medium transition-all ${
              mode === 'homework_based'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Based on Homework
          </button>
        </div>
      </div>

      {/* Common Controls */}
      <div className="bg-white rounded-xl shadow-sm p-6 border space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Difficulty Level
          </label>
          <input
            type="range"
            min="1"
            max="4"
            value={difficultyLevel}
            onChange={(e) => setDifficultyLevel(parseInt(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-sm text-gray-600 mt-2">
            {difficultyLabels.map((label, index) => (
              <span
                key={label}
                className={index + 1 === difficultyLevel ? 'font-semibold text-blue-600' : ''}
              >
                {label}
              </span>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Number of Questions
          </label>
          <input
            type="range"
            min="5"
            max="20"
            value={questionCount}
            onChange={(e) => setQuestionCount(parseInt(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-sm text-gray-600 mt-2">
            <span>5 questions</span>
            <span className="font-semibold text-blue-600">{questionCount} questions</span>
            <span>20 questions</span>
          </div>
        </div>
      </div>

      {/* Notes Selection UI */}
      {mode === 'notes_based' && (
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Class Notes</h2>
          {notes.length === 0 ? (
            <p className="text-gray-600">No class notes available for this subject.</p>
          ) : (
            <div className="space-y-3">
              {notes.map((note) => (
                <div
                  key={note.note_id}
                  className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    selectedNoteIds.includes(note.note_id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleNoteToggle(note.note_id)}
                >
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-5 h-5 rounded border-2 flex items-center justify-center mt-0.5 ${
                        selectedNoteIds.includes(note.note_id)
                          ? 'border-blue-500 bg-blue-500'
                          : 'border-gray-300'
                      }`}
                    >
                      {selectedNoteIds.includes(note.note_id) && (
                        <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{note.title}</p>
                      <p className="text-sm text-gray-600 mt-1">
                        {new Date(note.created_at).toLocaleDateString()}
                      </p>
                      {note.ocr_text && (
                        <p className="text-sm text-gray-500 mt-2 line-clamp-2">{note.ocr_text}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Homework Selection UI */}
      {mode === 'homework_based' && (
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Homework</h2>
          {homework.length === 0 ? (
            <p className="text-gray-600">No homework available for this subject.</p>
          ) : (
            <div className="space-y-3">
              {homework.map((hw) => (
                <div
                  key={hw.homework_id}
                  className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    selectedHomeworkIds.includes(hw.homework_id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleHomeworkToggle(hw.homework_id)}
                >
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-5 h-5 rounded border-2 flex items-center justify-center mt-0.5 ${
                        selectedHomeworkIds.includes(hw.homework_id)
                          ? 'border-blue-500 bg-blue-500'
                          : 'border-gray-300'
                      }`}
                    >
                      {selectedHomeworkIds.includes(hw.homework_id) && (
                        <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{hw.title}</p>
                      <p className="text-sm text-gray-600 mt-1">
                        {new Date(hw.created_at).toLocaleDateString()}
                      </p>
                      {hw.ocr_text && (
                        <p className="text-sm text-gray-500 mt-2 line-clamp-2">{hw.ocr_text}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Generate Button */}
      <div className="flex justify-end">
        <button
          onClick={handleGenerateTest}
          disabled={createTestMutation.isPending}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {createTestMutation.isPending ? (
            <span className="flex items-center gap-2">
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
              Generating Test...
            </span>
          ) : (
            'Generate Test'
          )}
        </button>
      </div>
    </div>
  );
}
