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

export default function SettingsPage() {
  const { token } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'prompts' | 'general'>('prompts');
  const [editingTemplate, setEditingTemplate] = useState<number | null>(null);
  const [editedPrompt, setEditedPrompt] = useState<string>('');

  // Fetch prompt templates from API
  const { data: templates, isLoading } = useQuery<PromptTemplate[]>({
    queryKey: ['prompt-templates'],
    queryFn: async () => {
      const response = await apiClient.get('/prompt-templates', {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    },
    enabled: !!token,
  });

  // Update template mutation
  const updateTemplateMutation = useMutation({
    mutationFn: async ({ templateId, promptTemplate }: { templateId: number; promptTemplate: string }) => {
      const response = await apiClient.put(
        `/prompt-templates/${templateId}`,
        { prompt_template: promptTemplate },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      return response.data;
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

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading settings...</p>
      </div>
    );
  }

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
