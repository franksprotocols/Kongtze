/**
 * Settings & Configuration Page
 * Configure AI prompts, system settings, and preferences
 */

'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { apiClient } from '@/lib/api-client';

interface PromptTemplate {
  template_id: number;
  template_name: string;
  template_type: string;
  prompt_template: string;
  description: string | null;
  is_active: boolean;
  is_system: boolean;
}

interface StudentProfile {
  profile_id: number;
  user_id: number;
  age: number;
  grade_level: string;
  school_name: string;
  math_proficiency: number;
  english_proficiency: number;
  chinese_proficiency: number;
  science_proficiency: number;
  strengths_weaknesses: {
    strengths: string[];
    weaknesses: string[];
  };
  learning_pace: string;
  notes: string | null;
}

interface TestResult {
  result_id: number;
  test_id: number;
  score: number;
  total_points: number;
  time_taken_seconds: number;
  submitted_at: string;
}

interface Note {
  note_id: number;
  title: string;
  subject_id: number;
  uploaded_at: string;
}

interface Homework {
  homework_id: number;
  title: string;
  subject_id: number;
  uploaded_at: string;
}

export default function SettingsPage() {
  const { token, user } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'prompts' | 'context' | 'general'>('prompts');
  const [editingTemplate, setEditingTemplate] = useState<number | null>(null);
  const [editedPrompt, setEditedPrompt] = useState<string>('');

  // Fetch prompt templates from API
  const { data: templates, isLoading: templatesLoading } = useQuery<PromptTemplate[]>({
    queryKey: ['prompt-templates'],
    queryFn: async () => {
      return await apiClient.get('/prompt-templates', token);
    },
    enabled: !!token,
  });

  // Fetch student profile
  const { data: profile, isLoading: profileLoading } = useQuery<StudentProfile>({
    queryKey: ['student-profile'],
    queryFn: async () => {
      return await apiClient.get(`/students/${user?.user_id}/profile`, token);
    },
    enabled: !!token && !!user && !user.is_parent,
  });

  // Fetch recent test results
  const { data: testResults, isLoading: testsLoading } = useQuery<TestResult[]>({
    queryKey: ['recent-test-results'],
    queryFn: async () => {
      return await apiClient.get('/test-results?limit=5', token);
    },
    enabled: !!token && activeTab === 'context',
  });

  // Fetch recent notes
  const { data: notes, isLoading: notesLoading } = useQuery<Note[]>({
    queryKey: ['recent-notes'],
    queryFn: async () => {
      return await apiClient.get('/notes?limit=5', token);
    },
    enabled: !!token && activeTab === 'context',
  });

  // Fetch recent homework
  const { data: homework, isLoading: homeworkLoading } = useQuery<Homework[]>({
    queryKey: ['recent-homework'],
    queryFn: async () => {
      return await apiClient.get('/homework?limit=5', token);
    },
    enabled: !!token && activeTab === 'context',
  });

  // Update template mutation
  const updateTemplateMutation = useMutation({
    mutationFn: async ({ templateId, promptTemplate }: { templateId: number; promptTemplate: string }) => {
      return await apiClient.put(
        `/prompt-templates/${templateId}`,
        { prompt_template: promptTemplate },
        token
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompt-templates'] });
      setEditingTemplate(null);
      setEditedPrompt('');
    },
  });

  const handleEditTemplate = (template: PromptTemplate) => {
    setEditingTemplate(template.template_id);
    setEditedPrompt(template.prompt_template);
  };

  const handleSaveTemplate = () => {
    if (editingTemplate) {
      updateTemplateMutation.mutate({
        templateId: editingTemplate,
        promptTemplate: editedPrompt,
      });
    }
  };

  const handleCancelEdit = () => {
    setEditingTemplate(null);
    setEditedPrompt('');
  };

  if (templatesLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading settings...</p>
      </div>
    );
  }

  const proficiencyLabel = (level: number) => {
    const labels = ['', 'Beginner', 'Average', 'Intermediate', 'Advanced'];
    return labels[level] || 'Unknown';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings & Configuration</h1>
        <p className="text-gray-600 mt-1">Manage AI prompts and system preferences</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('prompts')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'prompts'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            AI Prompts
          </button>
          <button
            onClick={() => setActiveTab('context')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'context'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Generation Context
          </button>
          <button
            onClick={() => setActiveTab('general')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'general'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            General Settings
          </button>
        </nav>
      </div>

      {/* AI Prompts Tab */}
      {activeTab === 'prompts' && (
        <div className="space-y-6">
          {templates?.map((template) => (
            <div key={template.template_id} className="bg-white rounded-xl shadow-sm p-6 border">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="flex items-center gap-3">
                    <h2 className="text-lg font-semibold text-gray-900">{template.template_name}</h2>
                    {template.is_system && (
                      <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded-full">
                        System Template
                      </span>
                    )}
                    {!template.is_active && (
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                        Inactive
                      </span>
                    )}
                  </div>
                  {template.description && (
                    <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                  )}
                  <p className="text-xs text-gray-500 mt-1">Type: {template.template_type}</p>
                </div>
                {editingTemplate !== template.template_id && (
                  <button
                    onClick={() => handleEditTemplate(template)}
                    className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Edit Prompt
                  </button>
                )}
              </div>

              {editingTemplate === template.template_id ? (
                <div className="space-y-4">
                  <textarea
                    value={editedPrompt}
                    onChange={(e) => setEditedPrompt(e.target.value)}
                    rows={20}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  />
                  <div className="flex gap-3">
                    <button
                      onClick={handleSaveTemplate}
                      disabled={updateTemplateMutation.isPending}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                    >
                      {updateTemplateMutation.isPending ? 'Saving...' : 'Save Changes'}
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
                    {template.prompt_template}
                  </pre>
                </div>
              )}

              <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h3 className="text-sm font-semibold text-blue-900 mb-2">Template Variables:</h3>
                <p className="text-xs text-blue-800">
                  Variables are enclosed in curly braces like {'{variable_name}'}. The system will automatically
                  replace these with actual values when generating content.
                </p>
              </div>
            </div>
          ))}

          {templates?.length === 0 && (
            <div className="text-center py-12 bg-white rounded-xl shadow-sm border">
              <p className="text-gray-600">No prompt templates found.</p>
              <p className="text-sm text-gray-500 mt-2">
                Run the seed script to create default templates.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Generation Context Tab */}
      {activeTab === 'context' && (
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-blue-900 mb-2">About Generation Context</h3>
            <p className="text-sm text-blue-800">
              These parameters are automatically used by the AI when generating tests, schedules, and other content.
              They provide personalized context to create content tailored to your learning needs.
            </p>
          </div>

          {/* Student Profile */}
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Student Profile</h2>
            {profileLoading ? (
              <p className="text-gray-600">Loading profile...</p>
            ) : profile ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Age</p>
                    <p className="font-medium">{profile.age} years old</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Grade Level</p>
                    <p className="font-medium">{profile.grade_level}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">School</p>
                    <p className="font-medium">{profile.school_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Learning Pace</p>
                    <p className="font-medium capitalize">{profile.learning_pace}</p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h3 className="text-sm font-semibold text-gray-900 mb-3">Subject Proficiency</h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Math:</span>
                      <span className="text-sm font-medium">{proficiencyLabel(profile.math_proficiency)}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">English:</span>
                      <span className="text-sm font-medium">{proficiencyLabel(profile.english_proficiency)}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Chinese:</span>
                      <span className="text-sm font-medium">{proficiencyLabel(profile.chinese_proficiency)}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Science:</span>
                      <span className="text-sm font-medium">{proficiencyLabel(profile.science_proficiency)}</span>
                    </div>
                  </div>
                </div>

                {profile.strengths_weaknesses && (
                  <div className="border-t pt-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <h3 className="text-sm font-semibold text-green-900 mb-2">Strengths</h3>
                        <ul className="space-y-1">
                          {profile.strengths_weaknesses.strengths?.map((strength, idx) => (
                            <li key={idx} className="text-sm text-gray-700 flex items-start">
                              <span className="text-green-600 mr-2">✓</span>
                              {strength}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h3 className="text-sm font-semibold text-orange-900 mb-2">Areas for Improvement</h3>
                        <ul className="space-y-1">
                          {profile.strengths_weaknesses.weaknesses?.map((weakness, idx) => (
                            <li key={idx} className="text-sm text-gray-700 flex items-start">
                              <span className="text-orange-600 mr-2">→</span>
                              {weakness}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                {profile.notes && (
                  <div className="border-t pt-4">
                    <h3 className="text-sm font-semibold text-gray-900 mb-2">Additional Notes</h3>
                    <p className="text-sm text-gray-700">{profile.notes}</p>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-600">No profile found. A default profile will be created on first use.</p>
            )}
          </div>

          {/* Recent Test Results */}
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Test Performance</h2>
            {testsLoading ? (
              <p className="text-gray-600">Loading test results...</p>
            ) : testResults && testResults.length > 0 ? (
              <div className="space-y-3">
                {testResults.map((result) => (
                  <div key={result.result_id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium">Test #{result.test_id}</p>
                      <p className="text-xs text-gray-600">
                        {new Date(result.submitted_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-semibold">
                        {result.score}/{result.total_points}
                      </p>
                      <p className="text-xs text-gray-600">
                        {Math.round((result.score / result.total_points) * 100)}%
                      </p>
                    </div>
                  </div>
                ))}
                <p className="text-xs text-gray-500 mt-2">
                  These results are used to adapt difficulty and question types.
                </p>
              </div>
            ) : (
              <p className="text-gray-600">No test results yet. Complete some tests to see your performance history.</p>
            )}
          </div>

          {/* Recent Notes */}
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Class Notes</h2>
            {notesLoading ? (
              <p className="text-gray-600">Loading notes...</p>
            ) : notes && notes.length > 0 ? (
              <div className="space-y-3">
                {notes.map((note) => (
                  <div key={note.note_id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium">{note.title}</p>
                      <p className="text-xs text-gray-600">
                        {new Date(note.uploaded_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
                <p className="text-xs text-gray-500 mt-2">
                  Recent notes are automatically used as context for test generation.
                </p>
              </div>
            ) : (
              <p className="text-gray-600">No notes uploaded yet. Upload class notes to improve test relevance.</p>
            )}
          </div>

          {/* Recent Homework */}
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Homework</h2>
            {homeworkLoading ? (
              <p className="text-gray-600">Loading homework...</p>
            ) : homework && homework.length > 0 ? (
              <div className="space-y-3">
                {homework.map((hw) => (
                  <div key={hw.homework_id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium">{hw.title}</p>
                      <p className="text-xs text-gray-600">
                        {new Date(hw.uploaded_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
                <p className="text-xs text-gray-500 mt-2">
                  Recent homework is automatically used as context for test generation.
                </p>
              </div>
            ) : (
              <p className="text-gray-600">No homework uploaded yet. Upload homework to improve test relevance.</p>
            )}
          </div>
        </div>
      )}

      {/* General Settings Tab */}
      {activeTab === 'general' && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">General Settings</h2>
            <p className="text-gray-600">General settings coming soon...</p>
          </div>
        </div>
      )}
    </div>
  );
}
