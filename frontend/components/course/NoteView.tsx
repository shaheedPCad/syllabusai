'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Download } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import type { StudyNoteResponse } from '@/services/study';

interface NoteViewProps {
  data: StudyNoteResponse;
  onBack: () => void;
}

export function NoteView({ data, onBack }: NoteViewProps) {
  const handleDownload = () => {
    const blob = new Blob([data.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.document_name}_${data.mode}_notes.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Study Hub
        </Button>
        <Button variant="outline" onClick={handleDownload}>
          <Download className="mr-2 h-4 w-4" />
          Download
        </Button>
      </div>

      {/* Note Content */}
      <Card>
        <CardHeader>
          <CardTitle>
            {data.mode === 'brief' ? '📝 Brief Review' : '📖 Deep Dive'}
          </CardTitle>
          <p className="text-sm text-muted-foreground">{data.document_name}</p>
        </CardHeader>
        <CardContent>
          {/* Markdown rendering with prose styling */}
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <ReactMarkdown>{data.content}</ReactMarkdown>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
