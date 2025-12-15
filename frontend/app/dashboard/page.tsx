'use client';

/**
 * Dashboard Test Page
 *
 * Simple test page to verify backend connection
 * - Fetches courses from API
 * - Displays raw JSON response
 * - Allows switching between student and teacher users
 */

import { useEffect, useState } from 'react';
import { getCourses } from '@/services/courses';
import { getUserEmail, setUserEmail } from '@/lib/api';
import type { Course } from '@/services/courses';

export default function DashboardPage() {
  const [courses, setCourses] = useState<Course[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<string>('');

  // Fetch courses on mount and when user changes
  useEffect(() => {
    fetchCourses();
    setCurrentUser(getUserEmail());
  }, []);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCourses();
      setCourses(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch courses');
      setCourses(null);
    } finally {
      setLoading(false);
    }
  };

  // Toggle between student and teacher users
  const toggleUser = () => {
    const newUser = currentUser === 'student@clarity.com'
      ? 'teacher@clarity.com'
      : 'student@clarity.com';

    setUserEmail(newUser);
    setCurrentUser(newUser);

    // Refetch courses with new user
    fetchCourses();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Dashboard Test Page
          </h1>
          <p className="text-gray-600">
            Testing connection to Clarity LMS Backend API
          </p>
        </div>

        {/* User Control */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-1">
                Current User
              </h2>
              <p className="text-sm text-gray-600">
                {currentUser}
              </p>
            </div>
            <button
              onClick={toggleUser}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Switch to {currentUser === 'student@clarity.com' ? 'Teacher' : 'Student'}
            </button>
          </div>
        </div>

        {/* API Connection Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            API Connection
          </h2>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Base URL:</span>
              <span className="text-sm font-mono text-gray-900">
                {process.env.NEXT_PUBLIC_API_URL}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Status:</span>
              <span className={`text-sm font-semibold ${
                loading ? 'text-yellow-600' :
                error ? 'text-red-600' :
                'text-green-600'
              }`}>
                {loading ? 'Loading...' : error ? 'Error' : 'Connected'}
              </span>
            </div>
          </div>
        </div>

        {/* Courses Response */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Courses Response
            </h2>
            <button
              onClick={fetchCourses}
              className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
            >
              Refresh
            </button>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-red-800 mb-1">
                Error
              </h3>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Success State */}
          {courses && !loading && !error && (
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-sm text-green-800">
                  ✓ Successfully fetched {courses.length} course{courses.length !== 1 ? 's' : ''}
                </p>
              </div>

              {/* Raw JSON Display */}
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Raw JSON Response:
                </h3>
                <pre className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-auto text-xs">
                  {JSON.stringify(courses, null, 2)}
                </pre>
              </div>

              {/* Formatted Display */}
              {courses.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">
                    Formatted View:
                  </h3>
                  <div className="space-y-2">
                    {courses.map((course) => (
                      <div
                        key={course.id}
                        className="border border-gray-200 rounded-lg p-3"
                      >
                        <div className="flex items-start justify-between">
                          <div>
                            <h4 className="font-semibold text-gray-900">
                              {course.title}
                            </h4>
                            <p className="text-sm text-gray-600 mt-1">
                              {course.description}
                            </p>
                          </div>
                          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                            {course.course_code}
                          </span>
                        </div>
                        <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
                          <span>Join Code: <code className="bg-gray-100 px-1 py-0.5 rounded">{course.join_code}</code></span>
                          <span>ID: <code className="bg-gray-100 px-1 py-0.5 rounded">{course.id}</code></span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
