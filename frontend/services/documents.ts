/**
 * Document Service
 *
 * API calls for document management
 */

import { api } from '@/lib/api';

/**
 * Document interface matching backend DocumentRead schema
 */
export interface Document {
  id: string;
  course_id: string;
  filename: string;
  s3_key: string;
  mime_type: string;
  created_at: string;
}

/**
 * Get all documents for a course
 *
 * - Teachers see all documents they uploaded
 * - Students see all documents for enrolled courses
 *
 * @param courseId - Course UUID
 * @returns Array of documents
 */
export const getDocuments = async (courseId: string): Promise<Document[]> => {
  const response = await api.get(`/courses/${courseId}/documents`);
  return response.data;
};

/**
 * Upload a document to a course (teachers only)
 *
 * @param courseId - Course UUID
 * @param file - File to upload
 * @returns Created document
 */
export const uploadDocument = async (
  courseId: string,
  file: File
): Promise<Document> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post(`/courses/${courseId}/documents`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Delete a document (teachers only)
 *
 * @param documentId - Document UUID
 * @returns void (204 No Content)
 */
export const deleteDocument = async (documentId: string): Promise<void> => {
  await api.delete(`/documents/${documentId}`);
};

/**
 * Get a specific document by ID
 *
 * @param documentId - Document UUID
 * @returns Document details
 */
export const getDocument = async (documentId: string): Promise<Document> => {
  const response = await api.get(`/documents/${documentId}`);
  return response.data;
};
