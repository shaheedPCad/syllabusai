'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, AlertCircle } from 'lucide-react';
import { getUserEmail } from '@/lib/api';
import { getDocuments, deleteDocument } from '@/services/documents';
import type { Document } from '@/services/documents';
import { UploadZone } from './UploadZone';
import { DocumentList } from './DocumentList';
import { Separator } from '@/components/ui/separator';

export function DocumentsView() {
  const params = useParams();
  const courseId = params.courseId as string;

  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<string>('');

  // Determine if user is a teacher
  const isTeacher = currentUser.includes('teacher');

  // Fetch documents
  const fetchDocuments = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getDocuments(courseId);
      setDocuments(data);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string };
      setError(error.response?.data?.detail || error.message || 'Failed to fetch documents');
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  // Handle delete
  const handleDelete = async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      // Refresh list
      await fetchDocuments();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string };
      alert(error.response?.data?.detail || error.message || 'Failed to delete document');
      throw err; // Re-throw so DocumentList knows it failed
    }
  };

  // Fetch on mount
  useEffect(() => {
    setCurrentUser(getUserEmail());
    if (courseId) {
      fetchDocuments();
    }
  }, [courseId, fetchDocuments]);

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-6">
        <div className="flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-destructive mt-0.5" />
          <div>
            <h3 className="font-semibold text-destructive mb-1">Error Loading Documents</h3>
            <p className="text-sm text-destructive/90">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Upload Zone (Teachers Only) */}
      {isTeacher && (
        <>
          <div>
            <h2 className="text-xl font-semibold mb-1">Upload Documents</h2>
            <p className="text-sm text-muted-foreground mb-4">
              Upload course materials that will be processed for AI-powered features
            </p>
            <UploadZone courseId={courseId} onUploadSuccess={fetchDocuments} />
          </div>
          <Separator />
        </>
      )}

      {/* Document List (All Users) */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          {isTeacher ? 'Uploaded Documents' : 'Course Materials'}
        </h2>
        <DocumentList
          documents={documents}
          isTeacher={isTeacher}
          onDelete={handleDelete}
        />
      </div>
    </div>
  );
}
