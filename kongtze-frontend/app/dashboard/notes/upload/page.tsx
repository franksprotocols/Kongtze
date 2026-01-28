/**
 * Class Notes Upload Page
 * Upload class notes with AI topic extraction
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useAuth } from '@/contexts/auth-context';
import { classNotesAPI, subjectsAPI } from '@/lib/api';
import Image from 'next/image';

export default function NotesUploadPage() {
  const router = useRouter();
  const { token } = useAuth();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [subjectId, setSubjectId] = useState(1);
  const [title, setTitle] = useState('');

  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectsAPI.getAll(token!),
    enabled: !!token,
  });

  const uploadMutation = useMutation({
    mutationFn: ({ subjectId, title, photo }: { subjectId: number; title: string; photo: File }) =>
      classNotesAPI.upload(subjectId, title, photo, token!),
    onSuccess: () => {
      router.push('/dashboard/notes');
    },
  });

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);

      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedFile && title) {
      uploadMutation.mutate({ subjectId, title, photo: selectedFile });
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Upload Class Notes</h1>
        <p className="text-gray-600 mt-2">
          Take a photo of your class notes and AI will extract topics
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Subject Selection */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Subject
          </label>
          <select
            value={subjectId}
            onChange={(e) => setSubjectId(parseInt(e.target.value))}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {subjects.map((subject) => (
              <option key={subject.subject_id} value={subject.subject_id}>
                {subject.display_name}
              </option>
            ))}
          </select>
        </div>

        {/* Title Input */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Notes Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g., Chapter 5 - Photosynthesis"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        {/* File Upload */}
        <div className="bg-white rounded-xl shadow-sm p-6 border">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Upload Photo
          </label>

          {!selectedFile ? (
            <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  className="w-12 h-12 text-gray-400 mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <p className="mb-2 text-sm text-gray-700">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500">PNG, JPG, or JPEG (MAX. 10MB)</p>
              </div>
              <input
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleFileSelect}
                required
              />
            </label>
          ) : (
            <div className="space-y-4">
              <div className="relative w-full h-96 bg-gray-100 rounded-lg overflow-hidden">
                <Image
                  src={previewUrl}
                  alt="Notes preview"
                  fill
                  className="object-contain"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setSelectedFile(null);
                    setPreviewUrl('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Remove Photo
                </button>
                <label className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-center cursor-pointer hover:bg-gray-200">
                  Choose Different Photo
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleFileSelect}
                  />
                </label>
              </div>
            </div>
          )}
        </div>

        {/* Submit Buttons */}
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
            disabled={!selectedFile || !title || uploadMutation.isPending}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploadMutation.isPending ? (
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
                Processing with AI...
              </span>
            ) : (
              '📝 Upload Notes'
            )}
          </button>
        </div>
      </form>

      {/* Error Display */}
      {uploadMutation.isError && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <p className="font-medium">Failed to upload notes</p>
          <p className="text-sm mt-1">
            {(uploadMutation.error as any)?.detail || 'Please try again'}
          </p>
        </div>
      )}
    </div>
  );
}

