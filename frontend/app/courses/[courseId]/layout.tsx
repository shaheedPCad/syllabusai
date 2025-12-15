'use client';

import { useEffect, useState } from 'react';
import { useParams, usePathname } from 'next/navigation';
import Link from 'next/link';
import { getCourse } from '@/services/courses';
import type { Course } from '@/services/courses';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
} from '@/components/ui/sidebar';
import { MessageSquare, FileText, Lightbulb, ArrowLeft, Loader2 } from 'lucide-react';
import { Separator } from '@/components/ui/separator';

export default function CourseLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const params = useParams();
  const pathname = usePathname();
  const courseId = params.courseId as string;

  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getCourse(courseId);
        setCourse(data);
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } }; message?: string };
        setError(error.response?.data?.detail || error.message || 'Failed to fetch course');
      } finally {
        setLoading(false);
      }
    };

    if (courseId) {
      fetchCourse();
    }
  }, [courseId]);

  const navigationItems = [
    {
      title: 'Chat',
      href: `/courses/${courseId}/chat`,
      icon: MessageSquare,
      description: 'Ask questions about course materials',
    },
    {
      title: 'Documents',
      href: `/courses/${courseId}/documents`,
      icon: FileText,
      description: 'Upload and manage course documents',
    },
    {
      title: 'Study',
      href: `/courses/${courseId}/study`,
      icon: Lightbulb,
      description: 'Flashcards and quizzes',
    },
  ];

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        {/* Sidebar */}
        <Sidebar collapsible="icon">
          <SidebarContent>
            <SidebarGroup>
              {/* Course Header */}
              <div className="px-3 py-4">
                {loading ? (
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm text-muted-foreground">Loading...</span>
                  </div>
                ) : error ? (
                  <div className="text-sm text-destructive">Error loading course</div>
                ) : course ? (
                  <div>
                    <h2 className="text-sm font-semibold line-clamp-2 group-data-[collapsible=icon]:hidden">
                      {course.title}
                    </h2>
                    <p className="text-xs text-muted-foreground mt-1 group-data-[collapsible=icon]:hidden">
                      {course.course_code}
                    </p>
                  </div>
                ) : null}
              </div>

              <Separator />

              {/* Navigation Items */}
              <SidebarGroupContent className="mt-4">
                <SidebarMenu>
                  {navigationItems.map((item) => {
                    const isActive = pathname.startsWith(item.href);
                    return (
                      <SidebarMenuItem key={item.title}>
                        <SidebarMenuButton
                          asChild
                          isActive={isActive}
                          tooltip={item.title}
                        >
                          <Link href={item.href}>
                            <item.icon className="h-4 w-4" />
                            <span>{item.title}</span>
                          </Link>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    );
                  })}
                </SidebarMenu>
              </SidebarGroupContent>
            </SidebarGroup>
          </SidebarContent>

          {/* Footer */}
          <SidebarFooter>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild tooltip="Back to Dashboard">
                  <Link href="/dashboard">
                    <ArrowLeft className="h-4 w-4" />
                    <span>Back to Dashboard</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarFooter>
        </Sidebar>

        {/* Main Content Area */}
        <SidebarInset>
          <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="mr-2 h-4" />
            {course && (
              <div className="flex flex-col">
                <h1 className="text-lg font-semibold">{course.title}</h1>
              </div>
            )}
          </header>
          <div className="flex flex-1 flex-col gap-4 p-4">
            {children}
          </div>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
}
