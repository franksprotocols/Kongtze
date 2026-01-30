/**
 * Protected dashboard layout with navigation
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/auth-context';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { isAuthenticated, isLoading, user, logout } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">Kongtze</h1>
            </div>

            <div className="flex items-center gap-6">
              <Link
                href="/dashboard"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Dashboard
              </Link>
              <Link
                href="/dashboard/calendar"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Calendar
              </Link>
              <Link
                href="/dashboard/tests"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Tests
              </Link>
              <Link
                href="/dashboard/homework"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Homework
              </Link>
              <Link
                href="/dashboard/notes"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Notes
              </Link>
              <Link
                href="/dashboard/rewards"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Rewards
              </Link>
              <Link
                href="/dashboard/settings"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                ⚙️ Settings
              </Link>
              {user?.is_parent && (
                <Link
                  href="/dashboard/students"
                  className="text-gray-700 hover:text-blue-600 font-medium"
                >
                  Students
                </Link>
              )}

              <div className="flex items-center gap-3 ml-4 border-l pl-4">
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                  <p className="text-xs text-gray-500">
                    {user?.is_parent ? 'Parent' : 'Student'}
                  </p>
                </div>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-red-600"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
