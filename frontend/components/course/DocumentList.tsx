'use client';

import { useState } from 'react';
import { format } from 'date-fns';
import { Trash2, FileText, Loader2 } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { Document } from '@/services/documents';

interface DocumentListProps {
  documents: Document[];
  isTeacher: boolean;
  onDelete: (documentId: string) => Promise<void>;
}

export function DocumentList({ documents, isTeacher, onDelete }: DocumentListProps) {
  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean;
    document: Document | null;
  }>({ open: false, document: null });
  const [deleting, setDeleting] = useState(false);

  // Handle delete confirmation
  const handleDeleteClick = (document: Document) => {
    setDeleteDialog({ open: true, document });
  };

  const handleDeleteConfirm = async () => {
    if (!deleteDialog.document) return;

    try {
      setDeleting(true);
      await onDelete(deleteDialog.document.id);
      setDeleteDialog({ open: false, document: null });
    } catch (err) {
      console.error('Failed to delete document:', err);
      // Error handled by parent
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialog({ open: false, document: null });
  };

  // Format date
  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), 'MMM d, yyyy h:mm a');
    } catch {
      return dateString;
    }
  };

  // Get file icon based on mime type
  const getFileIcon = () => {
    return <FileText className="h-4 w-4 text-muted-foreground" />;
  };

  // Empty state
  if (documents.length === 0) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <div className="p-4 bg-muted rounded-full mb-4">
            <FileText className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold mb-2">No documents yet</h3>
          <p className="text-sm text-muted-foreground text-center max-w-sm">
            {isTeacher
              ? 'Upload your syllabus, lecture notes, or other course materials to get started.'
              : "Your teacher hasn't uploaded any documents yet."}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            Course Documents ({documents.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[50px]"></TableHead>
                  <TableHead>Filename</TableHead>
                  <TableHead className="hidden md:table-cell">Upload Date</TableHead>
                  {isTeacher && <TableHead className="w-[100px]">Actions</TableHead>}
                </TableRow>
              </TableHeader>
              <TableBody>
                {documents.map((document) => (
                  <TableRow key={document.id}>
                    <TableCell>{getFileIcon()}</TableCell>
                    <TableCell className="font-medium">
                      <div className="flex flex-col">
                        <span>{document.filename}</span>
                        <span className="md:hidden text-xs text-muted-foreground">
                          {formatDate(document.created_at)}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell className="hidden md:table-cell text-muted-foreground">
                      {formatDate(document.created_at)}
                    </TableCell>
                    {isTeacher && (
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteClick(document)}
                          className="text-destructive hover:text-destructive hover:bg-destructive/10"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialog.open}
        onOpenChange={(open) =>
          !deleting && setDeleteDialog({ open, document: deleteDialog.document })
        }
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Document</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete &quot;{deleteDialog.document?.filename}&quot;?
              This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={handleDeleteCancel}
              disabled={deleting}
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteConfirm}
              disabled={deleting}
            >
              {deleting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Deleting...
                </>
              ) : (
                'Delete'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
