'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { MessageSquare, Sparkles } from 'lucide-react';

export function ChatView() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <Card className="max-w-2xl w-full">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/10 rounded-lg">
              <MessageSquare className="h-8 w-8 text-primary" />
            </div>
            <div>
              <CardTitle className="text-2xl">Chat with Course Materials</CardTitle>
              <CardDescription className="mt-1">
                AI-powered Q&A using RAG (Retrieval-Augmented Generation)
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-muted rounded-lg p-6 space-y-3">
            <div className="flex items-start gap-3">
              <Sparkles className="h-5 w-5 text-primary mt-0.5" />
              <div>
                <h3 className="font-semibold mb-1">Coming Soon</h3>
                <p className="text-sm text-muted-foreground">
                  The Chat interface is currently under development. Soon you'll be able to:
                </p>
              </div>
            </div>
            <ul className="ml-8 space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span>Ask questions about your course materials</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span>Get AI-powered answers based on uploaded documents</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span>View source citations for every response</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary">•</span>
                <span>Maintain conversation history for context</span>
              </li>
            </ul>
          </div>

          <div className="pt-4 text-center text-sm text-muted-foreground">
            This feature will integrate with the Documents you upload to provide intelligent, contextual answers.
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
