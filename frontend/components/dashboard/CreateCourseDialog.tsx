'use client';

import { useState, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { createCourse } from '@/services/courses';
import { PlusCircle, Loader2 } from 'lucide-react';

// Validation schema
const courseSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  course_code: z.string().min(2, 'Course code must be at least 2 characters').optional().or(z.literal('')),
});

type CourseFormData = z.infer<typeof courseSchema>;

interface CreateCourseDialogProps {
  onCourseCreated: () => void;
}

export function CreateCourseDialog({ onCourseCreated }: CreateCourseDialogProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const isSubmittingRef = useRef(false); // Prevent double-submit

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CourseFormData>({
    resolver: zodResolver(courseSchema),
  });

  const onSubmit = async (data: CourseFormData) => {
    // Prevent double-submit with synchronous check
    if (isSubmittingRef.current) {
      return;
    }

    try {
      isSubmittingRef.current = true;
      setLoading(true);
      await createCourse({
        title: data.title,
        description: data.description,
        course_code: data.course_code || `COURSE${Date.now().toString(36).toUpperCase()}`,
      });

      // Success
      setOpen(false);
      reset();
      onCourseCreated();
    } catch (err: unknown) {
      console.error('Failed to create course:', err);
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to create course');
    } finally {
      setLoading(false);
      isSubmittingRef.current = false;
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <PlusCircle className="mr-2 h-4 w-4" />
          Create Course
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Create New Course</DialogTitle>
            <DialogDescription>
              Create a new course. Students will be able to join using the generated code.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Title Field */}
            <div className="grid gap-2">
              <Label htmlFor="title">Course Title *</Label>
              <Input
                id="title"
                placeholder="e.g., Introduction to Computer Science"
                {...register('title')}
              />
              {errors.title && (
                <p className="text-sm text-destructive">{errors.title.message}</p>
              )}
            </div>

            {/* Description Field */}
            <div className="grid gap-2">
              <Label htmlFor="description">Description *</Label>
              <Input
                id="description"
                placeholder="A brief overview of the course"
                {...register('description')}
              />
              {errors.description && (
                <p className="text-sm text-destructive">{errors.description.message}</p>
              )}
            </div>

            {/* Course Code Field (Optional) */}
            <div className="grid gap-2">
              <Label htmlFor="course_code">Course Code (Optional)</Label>
              <Input
                id="course_code"
                placeholder="e.g., CS101 (auto-generated if empty)"
                {...register('course_code')}
              />
              {errors.course_code && (
                <p className="text-sm text-destructive">{errors.course_code.message}</p>
              )}
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating...
                </>
              ) : (
                'Create Course'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
