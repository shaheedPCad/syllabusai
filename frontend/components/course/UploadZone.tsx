'use client';

import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { Upload, Loader2, CheckCircle2, AlertCircle, FileText } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { uploadDocument } from '@/services/documents';

interface UploadZoneProps {
  courseId: string;
  onUploadSuccess: () => void;
}

export function UploadZone({ courseId, onUploadSuccess }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<{
    type: 'success' | 'error' | null;
    message: string;
  }>({ type: null, message: '' });

  const fileInputRef = useRef<HTMLInputElement>(null);

  // File validation
  const validateFile = (file: File): string | null => {
    // Max 50MB
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
      return 'File size must be less than 50MB';
    }

    // Allowed types
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
      'text/plain',
    ];

    if (!allowedTypes.includes(file.type)) {
      return 'File type not supported. Please upload PDF, DOCX, DOC, or TXT files.';
    }

    return null;
  };

  // Handle file upload
  const handleUpload = async (file: File) => {
    // Validate
    const error = validateFile(file);
    if (error) {
      setUploadStatus({ type: 'error', message: error });
      setTimeout(() => setUploadStatus({ type: null, message: '' }), 5000);
      return;
    }

    try {
      setUploading(true);
      setUploadStatus({ type: null, message: '' });

      await uploadDocument(courseId, file);

      // Success
      setUploadStatus({
        type: 'success',
        message: `${file.name} uploaded successfully!`,
      });

      // Clear after 3 seconds
      setTimeout(() => setUploadStatus({ type: null, message: '' }), 3000);

      // Trigger refresh
      onUploadSuccess();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string };
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || error.message || 'Failed to upload document',
      });
    } finally {
      setUploading(false);
    }
  };

  // Drag & drop handlers
  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleUpload(files[0]);
    }
  };

  // Click to upload
  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleUpload(files[0]);
    }
    // Reset input to allow re-upload of same file
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-3">
      <Card
        className={`border-2 border-dashed transition-colors cursor-pointer ${
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-muted-foreground/25 hover:border-primary/50'
        }`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <CardContent className="flex flex-col items-center justify-center py-8 px-6">
          {uploading ? (
            <div className="flex flex-col items-center gap-3">
              <Loader2 className="h-10 w-10 text-primary animate-spin" />
              <p className="text-sm text-muted-foreground">Uploading...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3 text-center">
              <div className="p-3 bg-primary/10 rounded-full">
                <Upload className="h-8 w-8 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium">
                  Drag and drop your file here, or click to browse
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  PDF, DOCX, DOC, or TXT (max 50MB)
                </p>
              </div>
              <Button variant="secondary" size="sm" className="mt-2">
                <FileText className="mr-2 h-4 w-4" />
                Choose File
              </Button>
            </div>
          )}

          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileChange}
            className="hidden"
          />
        </CardContent>
      </Card>

      {/* Status Messages */}
      {uploadStatus.type === 'success' && (
        <div className="flex items-center gap-2 p-3 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
          <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400" />
          <p className="text-sm text-green-800 dark:text-green-200">{uploadStatus.message}</p>
        </div>
      )}

      {uploadStatus.type === 'error' && (
        <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg">
          <AlertCircle className="h-4 w-4 text-red-600 dark:text-red-400" />
          <p className="text-sm text-red-800 dark:text-red-200">{uploadStatus.message}</p>
        </div>
      )}
    </div>
  );
}
