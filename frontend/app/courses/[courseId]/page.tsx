'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';

export default function CoursePage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;

  useEffect(() => {
    // Redirect to chat view by default
    if (courseId) {
      router.replace(`/courses/${courseId}/chat`);
    }
  }, [courseId, router]);

  return null;
}
