/**
 * Chat Service
 *
 * API calls for RAG-based chat with course materials
 */

import { api } from '@/lib/api';

/**
 * Document source interface matching backend DocumentSource schema
 */
export interface DocumentSource {
  chunk_id: string;
  text: string;
  similarity_score: number;
}

/**
 * Chat response interface matching backend ChatResponse schema
 */
export interface ChatResponse {
  answer: string;
  sources: DocumentSource[];
  confidence: 'low' | 'medium' | 'high';
}

/**
 * Ask a question about course materials using RAG
 *
 * - Searches through course documents using vector similarity
 * - Returns AI-generated answer with source citations
 * - Requires user to be enrolled in course (students) or own course (teachers)
 *
 * @param courseId - Course UUID
 * @param question - User's question (1-1000 chars)
 * @returns ChatResponse with answer, sources, and confidence level
 */
export const askQuestion = async (
  courseId: string,
  question: string
): Promise<ChatResponse> => {
  const response = await api.post(`/courses/${courseId}/chat`, {
    question,
  });
  return response.data;
};
