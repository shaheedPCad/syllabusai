'use client';

import { useParams } from 'next/navigation';
import { StudyView } from '@/components/course/StudyView';

export default function StudyPage() {
  const params = useParams();
  const courseId = params.courseId as string;

  if (!courseId) {
    return null;
  }

  return <StudyView courseId={courseId} />;
}
