import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BookOpen } from 'lucide-react';
import Link from 'next/link';
import type { Course } from '@/services/courses';

interface CourseCardProps {
  course: Course;
}

export function CourseCard({ course }: CourseCardProps) {
  return (
    <Card className="flex flex-col h-full hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            <CardTitle className="text-xl">{course.title}</CardTitle>
          </div>
          <span className="text-xs font-mono bg-primary/10 text-primary px-2 py-1 rounded">
            {course.course_code}
          </span>
        </div>
        <CardDescription className="line-clamp-2">
          {course.description}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col justify-end">
        <div className="flex flex-col gap-2">
          <div className="text-xs text-muted-foreground">
            Join Code: <code className="bg-muted px-1.5 py-0.5 rounded">{course.join_code}</code>
          </div>
          <Link href={`/courses/${course.id}`} className="w-full">
            <Button className="w-full">Enter Class</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
