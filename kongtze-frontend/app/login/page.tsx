/**
 * Login page with parent and student login options
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuth } from '@/contexts/auth-context';
import Link from 'next/link';

// Parent login schema
const parentLoginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

// Student login schema
const studentLoginSchema = z.object({
  pin: z.string().regex(/^\d{4}$/, 'PIN must be exactly 4 digits'),
});

type ParentLoginForm = z.infer<typeof parentLoginSchema>;
type StudentLoginForm = z.infer<typeof studentLoginSchema>;

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState<'parent' | 'student'>('parent');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { login } = useAuth();

  // Parent form
  const parentForm = useForm<ParentLoginForm>({
    resolver: zodResolver(parentLoginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  // Student form
  const studentForm = useForm<StudentLoginForm>({
    resolver: zodResolver(studentLoginSchema),
    defaultValues: {
      pin: '',
    },
  });

  const handleParentLogin = async (data: ParentLoginForm) => {
    setIsLoading(true);
    setError('');

    try {
      await login({ email: data.email, password: data.password });
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.detail || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStudentLogin = async (data: StudentLoginForm) => {
    setIsLoading(true);
    setError('');

    try {
      await login({ pin: data.pin });
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.detail || 'Invalid PIN');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Kongtze</h1>
          <p className="text-gray-600">AI-Powered Learning Platform</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Tab Switcher */}
          <div className="flex gap-2 mb-6 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setActiveTab('parent')}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                activeTab === 'parent'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Parent
            </button>
            <button
              onClick={() => setActiveTab('student')}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                activeTab === 'student'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Student
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          {/* Parent Login Form */}
          {activeTab === 'parent' && (
            <form onSubmit={parentForm.handleSubmit(handleParentLogin)}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    {...parentForm.register('email')}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="parent@example.com"
                  />
                  {parentForm.formState.errors.email && (
                    <p className="mt-1 text-sm text-red-600">
                      {parentForm.formState.errors.email.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Password
                  </label>
                  <input
                    type="password"
                    {...parentForm.register('password')}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your password"
                  />
                  {parentForm.formState.errors.password && (
                    <p className="mt-1 text-sm text-red-600">
                      {parentForm.formState.errors.password.message}
                    </p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? 'Logging in...' : 'Login as Parent'}
                </button>

                <p className="text-center text-sm text-gray-600">
                  Don't have an account?{' '}
                  <Link href="/register" className="text-blue-600 hover:underline">
                    Register
                  </Link>
                </p>
              </div>
            </form>
          )}

          {/* Student Login Form */}
          {activeTab === 'student' && (
            <form onSubmit={studentForm.handleSubmit(handleStudentLogin)}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Enter your 4-digit PIN
                  </label>
                  <input
                    type="text"
                    inputMode="numeric"
                    maxLength={4}
                    {...studentForm.register('pin')}
                    className="w-full px-4 py-3 text-center text-2xl tracking-widest border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="••••"
                  />
                  {studentForm.formState.errors.pin && (
                    <p className="mt-1 text-sm text-red-600">
                      {studentForm.formState.errors.pin.message}
                    </p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? 'Logging in...' : 'Login as Student'}
                </button>

                <p className="text-sm text-gray-600 text-center">
                  Ask your parent for your PIN
                </p>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
