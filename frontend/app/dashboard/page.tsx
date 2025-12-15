'use client';

import { useEffect, useState } from 'react';
import { getCourses } from '@/services/courses';
import { getUserEmail } from '@/lib/api';
import type { Course } from '@/services/courses';
import { CourseCard } from '@/components/dashboard/CourseCard';
import { CreateCourseDialog } from '@/components/dashboard/CreateCourseDialog';
import { JoinCourse } from '@/components/dashboard/JoinCourse';
import { Loader2, BookOpen } from 'lucide-react';

export default function DashboardPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<string>('');

  // Fetch courses on mount
  useEffect(() => {
    setCurrentUser(getUserEmail());
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCourses();
      setCourses(data);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string };
      setError(error.response?.data?.detail || error.message || 'Failed to fetch courses');
    } finally {
      setLoading(false);
    }
  };

  const isTeacher = currentUser.includes('teacher');

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col gap-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">My Courses</h1>
              <p className="text-muted-foreground mt-1">
                {isTeacher ? 'Manage your courses' : 'Your enrolled courses'}
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-3">
              {isTeacher ? (
                <CreateCourseDialog onCourseCreated={fetchCourses} />
              ) : (
                <JoinCourse onCourseJoined={fetchCourses} />
              )}
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && courses.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <BookOpen className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No courses found</h3>
            <p className="text-muted-foreground mb-4">
              {isTeacher
                ? 'Create your first course to get started.'
                : 'Join a course using a join code to get started.'}
            </p>
          </div>
        )}

        {/* Course Grid */}
        {!loading && !error && courses.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
