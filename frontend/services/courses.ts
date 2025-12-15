/**
 * Course Service
 *
 * API calls for course management
 */

import { api } from '@/lib/api';

/**
 * Course interface matching backend schema
 */
export interface Course {
  id: string;
  title: string;
  description: string;
  course_code: string;
  join_code: string;
  teacher_id: string;
  created_at: string;
}

/**
 * Create course request interface
 */
export interface CreateCourseRequest {
  title: string;
  description: string;
  course_code: string;
}

/**
 * Join course request interface
 */
export interface JoinCourseRequest {
  join_code: string;
}

/**
 * Get all courses for the current user
 *
 * - Teachers see courses they created
 * - Students see courses they're enrolled in
 *
 * @returns Array of courses
 */
export const getCourses = async (): Promise<Course[]> => {
  const response = await api.get('/courses');
  return response.data;
};

/**
 * Create a new course (teachers only)
 *
 * @param data - Course creation data
 * @returns Created course
 */
export const createCourse = async (data: CreateCourseRequest): Promise<Course> => {
  const response = await api.post('/courses', data);
  return response.data;
};

/**
 * Join a course using join code (students only)
 *
 * @param joinCode - 6-character join code
 * @returns Success message
 */
export const joinCourse = async (joinCode: string): Promise<{ message: string }> => {
  const response = await api.post(`/courses/join`, { join_code: joinCode });
  return response.data;
};

/**
 * Get a specific course by ID
 *
 * @param courseId - Course UUID
 * @returns Course details
 */
export const getCourse = async (courseId: string): Promise<Course> => {
  const response = await api.get(`/courses/${courseId}`);
  return response.data;
};
