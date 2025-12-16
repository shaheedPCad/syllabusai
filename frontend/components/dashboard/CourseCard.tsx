import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import Link from 'next/link';
import type { Course } from '@/services/courses';

interface CourseCardProps {
  course: Course;
}

export function CourseCard({ course }: CourseCardProps) {
  return (
    <div className="group bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hover:-translate-y-1 hover:shadow-md hover:border-blue-300 transition-all duration-300">
      {/* Card Header */}
      <div className="p-6">
        <div className="flex items-start justify-between gap-3 mb-3">
          <h3 className="text-xl font-semibold text-slate-900 line-clamp-1 flex-1">
            {course.title}
          </h3>
          <span className="bg-blue-50 text-blue-700 font-medium rounded-full px-3 py-1 text-xs whitespace-nowrap">
            {course.course_code}
          </span>
        </div>
        
        {/* Description */}
        <p className="text-slate-500 text-sm line-clamp-2 mt-2">
          {course.description}
        </p>
      </div>

      {/* Card Footer */}
      <div className="px-6 pb-6">
        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          <div className="text-xs text-slate-400">
            Code: <code className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-mono">{course.join_code}</code>
          </div>
        </div>
        
        <Link href={`/courses/${course.id}`} className="block mt-4">
          <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-2 font-medium shadow-sm transition-colors group">
            Enter Class
            <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
          </Button>
        </Link>
      </div>
    </div>
  );
}
