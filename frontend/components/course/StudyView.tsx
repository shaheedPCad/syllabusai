'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Loader2, FileText, BookOpen, Brain, Target } from 'lucide-react';
import { NoteView } from './NoteView';
import { FlashcardSession } from './FlashcardSession';
import { QuizSession } from './QuizSession';
import { getDocuments, type Document } from '@/services/courses';
import {
  generateStudyNote,
  generateFlashcards,
  generateQuiz,
  type StudyNoteResponse,
  type FlashcardResponse,
  type QuizResponse,
} from '@/services/study';

interface StudyViewProps {
  courseId: string;
}

type ViewMode = 'setup' | 'note' | 'flashcards' | 'quiz';

interface ModeCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  onClick: () => void;
  disabled: boolean;
  loading?: boolean;
  showCountInput?: boolean;
  count?: number;
  onCountChange?: (count: number) => void;
  countLabel?: string;
  countRange?: [number, number];
}

function ModeCard({
  icon: Icon,
  title,
  description,
  onClick,
  disabled,
  loading,
  showCountInput,
  count,
  onCountChange,
  countLabel,
  countRange,
}: ModeCardProps) {
  return (
    <Card className={`${!disabled && 'cursor-pointer hover:border-primary'} transition-all hover:shadow-md`}>
      <CardContent className="pt-6">
        <div className="flex flex-col items-center text-center space-y-3">
          <Icon className="h-12 w-12 text-primary" />
          <h3 className="font-semibold text-lg">{title}</h3>
          <p className="text-sm text-muted-foreground">{description}</p>

          {showCountInput && (
            <div className="w-full mt-2">
              <Label className="text-xs">{countLabel}</Label>
              <Input
                type="number"
                value={count}
                onChange={(e) => onCountChange?.(Number(e.target.value))}
                min={countRange?.[0]}
                max={countRange?.[1]}
                className="mt-1"
                disabled={disabled}
              />
            </div>
          )}

          <Button
            onClick={onClick}
            disabled={disabled}
            className="w-full mt-2"
          >
            {loading ? <Loader2 className="animate-spin h-4 w-4" /> : 'Generate'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

export function StudyView({ courseId }: StudyViewProps) {
  const [view, setView] = useState<ViewMode>('setup');
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Mode-specific state
  const [studyNoteData, setStudyNoteData] = useState<StudyNoteResponse | null>(null);
  const [flashcardData, setFlashcardData] = useState<FlashcardResponse | null>(null);
  const [quizData, setQuizData] = useState<QuizResponse | null>(null);

  // Configuration state
  const [flashcardCount, setFlashcardCount] = useState(10);
  const [quizCount, setQuizCount] = useState(5);

  // Load documents on mount
  useEffect(() => {
    const loadDocuments = async () => {
      try {
        setLoadingDocuments(true);
        const docs = await getDocuments(courseId);
        setDocuments(docs);
      } catch (err) {
        setError('Failed to load documents. Please try again.');
      } finally {
        setLoadingDocuments(false);
      }
    };

    loadDocuments();
  }, [courseId]);

  const handleGenerateBrief = async () => {
    if (!selectedDocumentId) return;

    try {
      setLoading(true);
      setError(null);
      const response = await generateStudyNote(selectedDocumentId, 'brief');
      setStudyNoteData(response);
      setView('note');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate brief note');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateThorough = async () => {
    if (!selectedDocumentId) return;

    try {
      setLoading(true);
      setError(null);
      const response = await generateStudyNote(selectedDocumentId, 'thorough');
      setStudyNoteData(response);
      setView('note');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate thorough note');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateFlashcards = async () => {
    if (!selectedDocumentId) return;

    try {
      setLoading(true);
      setError(null);
      const response = await generateFlashcards(selectedDocumentId, flashcardCount);
      setFlashcardData(response);
      setView('flashcards');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate flashcards');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateQuiz = async () => {
    if (!selectedDocumentId) return;

    try {
      setLoading(true);
      setError(null);
      const response = await generateQuiz(selectedDocumentId, quizCount);
      setQuizData(response);
      setView('quiz');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setView('setup');
    setStudyNoteData(null);
    setFlashcardData(null);
    setQuizData(null);
    setError(null);
  };

  // Setup view
  if (view === 'setup') {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Study Hub</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Document Selector */}
            <div>
              <Label>Select Document</Label>
              {loadingDocuments ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              ) : documents.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                  <p>No documents available. Upload a document first.</p>
                </div>
              ) : (
                <Select value={selectedDocumentId || ''} onValueChange={setSelectedDocumentId}>
                  <SelectTrigger className="mt-2">
                    <SelectValue placeholder="Choose a document to study" />
                  </SelectTrigger>
                  <SelectContent>
                    {documents.map((doc) => (
                      <SelectItem key={doc.id} value={doc.id}>
                        {doc.filename}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-destructive/10 text-destructive p-4 rounded-lg text-sm">
                {error}
              </div>
            )}

            {/* Mode Cards Grid */}
            {documents.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <ModeCard
                  icon={FileText}
                  title="Brief Review"
                  description="Quick cheat sheet with key concepts"
                  onClick={handleGenerateBrief}
                  disabled={!selectedDocumentId || loading}
                  loading={loading}
                />

                <ModeCard
                  icon={BookOpen}
                  title="Deep Dive"
                  description="Detailed lesson with examples"
                  onClick={handleGenerateThorough}
                  disabled={!selectedDocumentId || loading}
                  loading={loading}
                />

                <ModeCard
                  icon={Brain}
                  title="Flashcards"
                  description="Practice with Q&A cards"
                  onClick={handleGenerateFlashcards}
                  disabled={!selectedDocumentId || loading}
                  loading={loading}
                  showCountInput
                  count={flashcardCount}
                  onCountChange={setFlashcardCount}
                  countLabel="Number of Cards (5-20)"
                  countRange={[5, 20]}
                />

                <ModeCard
                  icon={Target}
                  title="Practice Quiz"
                  description="Test your knowledge"
                  onClick={handleGenerateQuiz}
                  disabled={!selectedDocumentId || loading}
                  loading={loading}
                  showCountInput
                  count={quizCount}
                  onCountChange={setQuizCount}
                  countLabel="Number of Questions (3-15)"
                  countRange={[3, 15]}
                />
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  // Session views
  if (view === 'note' && studyNoteData) {
    return <NoteView data={studyNoteData} onBack={handleBack} />;
  }

  if (view === 'flashcards' && flashcardData) {
    return <FlashcardSession data={flashcardData} onBack={handleBack} />;
  }

  if (view === 'quiz' && quizData) {
    return <QuizSession data={quizData} onBack={handleBack} />;
  }

  // Fallback
  return null;
}
