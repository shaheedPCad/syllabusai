'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Upload, FileCheck, Zap } from 'lucide-react';

export function DocumentsView() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <Card className="max-w-2xl w-full">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/10 rounded-lg">
              <FileText className="h-8 w-8 text-primary" />
            </div>
            <div>
              <CardTitle className="text-2xl">Course Documents</CardTitle>
              <CardDescription className="mt-1">
                Upload and manage PDFs, presentations, and study materials
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-muted rounded-lg p-6 space-y-3">
            <div className="flex items-start gap-3">
              <Upload className="h-5 w-5 text-primary mt-0.5" />
              <div>
                <h3 className="font-semibold mb-1">Coming Soon</h3>
                <p className="text-sm text-muted-foreground">
                  The Document Manager is currently under development. Soon you'll be able to:
                </p>
              </div>
            </div>
            <ul className="ml-8 space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <Upload className="h-4 w-4 text-primary mt-0.5" />
                <span>Upload PDFs, DOCX, and other course materials</span>
              </li>
              <li className="flex items-start gap-2">
                <FileCheck className="h-4 w-4 text-primary mt-0.5" />
                <span>View and organize all uploaded documents</span>
              </li>
              <li className="flex items-start gap-2">
                <Zap className="h-4 w-4 text-primary mt-0.5" />
                <span>Automatic text extraction and processing</span>
              </li>
              <li className="flex items-start gap-2">
                <FileText className="h-4 w-4 text-primary mt-0.5" />
                <span>Generate embeddings for AI-powered search</span>
              </li>
            </ul>
          </div>

          <div className="pt-4 text-center text-sm text-muted-foreground">
            Documents will be processed in the background and made available for Chat and Study features.
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
