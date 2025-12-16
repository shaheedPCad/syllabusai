/**
 * Study Service
 * API calls for study material generation (notes, flashcards, quizzes)
 */

import { api } from '@/lib/api';

// ============================================================================
// TypeScript Interfaces (matching backend schemas)
// ============================================================================

export interface Flashcard {
  front: string;
  back: string;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct_answer_index: number;
  explanation: string;
}

export interface StudyNoteResponse {
  note_id: string;
  document_id: string;
  document_name: string;
  mode: 'brief' | 'thorough';
  content: string; // Markdown
  created_at: string;
}

export interface FlashcardResponse {
  set_id: string;
  flashcards: Flashcard[];
  document_id: string;
  document_name: string;
  total_cards: number;
  created_at: string;
}

export interface QuizResponse {
  set_id: string;
  questions: QuizQuestion[];
  document_id: string;
  document_name: string;
  total_questions: number;
  created_at: string;
}

export interface StudyHistoryItem {
  id: string;
  type: 'note' | 'flashcards' | 'quiz';
  mode?: 'brief' | 'thorough';
  count?: number;
  created_at: string;
}

export interface StudyHistoryResponse {
  document_id: string;
  document_name: string;
  items: StudyHistoryItem[];
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Generate study note (brief or thorough)
 *
 * @param documentId - Document UUID
 * @param mode - "brief" for cheat sheet or "thorough" for detailed lesson
 * @returns StudyNoteResponse with generated note
 */
export const generateStudyNote = async (
  documentId: string,
  mode: 'brief' | 'thorough'
): Promise<StudyNoteResponse> => {
  const response = await api.post(`/documents/${documentId}/study-note`, {
    mode,
  });
  return response.data;
};

/**
 * Generate flashcards with configurable count
 *
 * @param documentId - Document UUID
 * @param count - Number of flashcards (5-20, default 10)
 * @returns FlashcardResponse with generated flashcards
 */
export const generateFlashcards = async (
  documentId: string,
  count: number = 10
): Promise<FlashcardResponse> => {
  const response = await api.post(`/documents/${documentId}/flashcards`, {
    count,
  });
  return response.data;
};

/**
 * Generate quiz with configurable count
 *
 * @param documentId - Document UUID
 * @param count - Number of quiz questions (3-15, default 5)
 * @returns QuizResponse with generated quiz
 */
export const generateQuiz = async (
  documentId: string,
  count: number = 5
): Promise<QuizResponse> => {
  const response = await api.post(`/documents/${documentId}/quiz`, {
    count,
  });
  return response.data;
};

/**
 * Get study note by ID
 *
 * @param noteId - Study note UUID
 * @returns StudyNoteResponse
 */
export const getStudyNote = async (
  noteId: string
): Promise<StudyNoteResponse> => {
  const response = await api.get(`/study-notes/${noteId}`);
  return response.data;
};

/**
 * Get flashcard set by ID
 *
 * @param setId - Flashcard set UUID
 * @returns FlashcardResponse
 */
export const getFlashcardSet = async (
  setId: string
): Promise<FlashcardResponse> => {
  const response = await api.get(`/flashcard-sets/${setId}`);
  return response.data;
};

/**
 * Get quiz set by ID
 *
 * @param setId - Quiz set UUID
 * @returns QuizResponse
 */
export const getQuizSet = async (
  setId: string
): Promise<QuizResponse> => {
  const response = await api.get(`/quiz-sets/${setId}`);
  return response.data;
};

/**
 * Get study history for a document
 *
 * @param documentId - Document UUID
 * @returns StudyHistoryResponse with all study materials
 */
export const getStudyHistory = async (
  documentId: string
): Promise<StudyHistoryResponse> => {
  const response = await api.get(`/documents/${documentId}/study-history`);
  return response.data;
};
