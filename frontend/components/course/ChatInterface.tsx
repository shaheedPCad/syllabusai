'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Loader2, Send, AlertCircle, User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { askQuestion } from '@/services/chat';
import type { ChatResponse, DocumentSource } from '@/services/chat';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: DocumentSource[];
  confidence?: 'low' | 'medium' | 'high';
}

export function ChatInterface() {
  const params = useParams();
  const courseId = params.courseId as string;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      const viewport = scrollAreaRef.current.querySelector(
        '[data-radix-scroll-area-viewport]'
      );
      if (viewport) {
        viewport.scrollTop = viewport.scrollHeight;
      }
    }
  }, [messages]);

  const handleSubmit = useCallback(
    async (e?: React.FormEvent) => {
      e?.preventDefault();

      const question = inputValue.trim();

      // Validation
      if (!question) return;
      if (question.length > 1000) {
        setError('Question must be less than 1000 characters');
        setTimeout(() => setError(null), 5000);
        return;
      }

      // Add user message
      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'user',
        content: question,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputValue('');
      setIsLoading(true);
      setError(null);

      try {
        const response: ChatResponse = await askQuestion(courseId, question);

        // Add assistant message
        const assistantMessage: ChatMessage = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: response.answer || 'I could not find an answer to your question.',
          timestamp: new Date(),
          sources: response.sources,
          confidence: response.confidence,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err: unknown) {
        const error = err as {
          response?: { data?: { detail?: string } };
          message?: string;
        };
        const errorMessage =
          error.response?.data?.detail ||
          error.message ||
          'Failed to get answer';

        setError(errorMessage);
        setTimeout(() => setError(null), 5000);
      } finally {
        setIsLoading(false);
        inputRef.current?.focus();
      }
    },
    [inputValue, courseId]
  );

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)]">
      <Card className="flex flex-col flex-1">
        {/* Header */}
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5 text-primary" />
            Chat with Course Materials
          </CardTitle>
        </CardHeader>

        {/* Messages Area */}
        <CardContent className="flex-1 flex flex-col min-h-0">
          <ScrollArea ref={scrollAreaRef} className="flex-1 pr-4">
            <div className="space-y-4">
              {messages.length === 0 ? (
                <EmptyState />
              ) : (
                messages.map((msg) => (
                  <MessageBubble key={msg.id} message={msg} />
                ))
              )}
              {isLoading && <LoadingIndicator />}
            </div>
          </ScrollArea>

          <Separator className="my-4" />

          {/* Input Area */}
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about course materials..."
              disabled={isLoading}
              className="flex-1"
              maxLength={1000}
            />
            <Button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              size="icon"
              aria-label="Send message"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>

          {/* Error Display */}
          {error && <ErrorBanner message={error} />}
        </CardContent>
      </Card>
    </div>
  );
}

// Sub-components

interface MessageBubbleProps {
  message: ChatMessage;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const [showSources, setShowSources] = useState(false);

  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-lg bg-primary px-4 py-2 text-primary-foreground">
          <div className="flex items-start gap-2">
            <p className="text-sm whitespace-pre-wrap break-words">
              {message.content}
            </p>
            <User className="h-4 w-4 mt-0.5 shrink-0" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-[80%] rounded-lg bg-muted px-4 py-2">
        <div className="flex items-start gap-2 mb-2">
          <Bot className="h-4 w-4 mt-0.5 text-primary shrink-0" />
          <div className="flex-1 prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        </div>

        {/* Confidence Badge */}
        {message.confidence && (
          <div className="mb-2">
            <ConfidenceBadge confidence={message.confidence} />
          </div>
        )}

        {/* Sources (Collapsible) */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 pt-2 border-t border-border">
            <button
              onClick={() => setShowSources(!showSources)}
              className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1 transition-colors"
            >
              <span>{showSources ? '▼' : '▶'}</span>
              <span>{message.sources.length} Source{message.sources.length > 1 ? 's' : ''}</span>
            </button>

            {showSources && (
              <div className="mt-2 space-y-1">
                {message.sources.map((source, idx) => (
                  <SourceItem
                    key={source.chunk_id}
                    source={source}
                    index={idx}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function ConfidenceBadge({
  confidence,
}: {
  confidence: 'low' | 'medium' | 'high';
}) {
  const colors = {
    low: 'bg-yellow-100 dark:bg-yellow-950 text-yellow-800 dark:text-yellow-200',
    medium:
      'bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-200',
    high: 'bg-green-100 dark:bg-green-950 text-green-800 dark:text-green-200',
  };

  return (
    <span className={`text-xs px-2 py-0.5 rounded-full ${colors[confidence]}`}>
      {confidence} confidence
    </span>
  );
}

function SourceItem({
  source,
  index,
}: {
  source: DocumentSource;
  index: number;
}) {
  return (
    <div className="text-xs bg-background/50 rounded p-2 border border-border">
      <div className="flex justify-between items-start mb-1">
        <span className="font-medium">Source {index + 1}</span>
        <span className="text-muted-foreground">
          {(source.similarity_score * 100).toFixed(0)}% match
        </span>
      </div>
      <p className="text-muted-foreground line-clamp-2">{source.text}</p>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <Bot className="h-12 w-12 text-muted-foreground mb-3" />
      <h3 className="text-lg font-semibold mb-1">Start a Conversation</h3>
      <p className="text-sm text-muted-foreground max-w-md">
        Ask questions about your course materials. I&apos;ll search through uploaded
        documents to provide accurate, cited answers.
      </p>
    </div>
  );
}

function LoadingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="max-w-[80%] rounded-lg bg-muted px-4 py-2">
        <div className="flex items-center gap-2">
          <Loader2 className="h-4 w-4 animate-spin text-primary" />
          <span className="text-sm text-muted-foreground">Thinking...</span>
        </div>
      </div>
    </div>
  );
}

function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="mt-2 flex items-start gap-2 p-3 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg">
      <AlertCircle className="h-4 w-4 text-red-600 dark:text-red-400 mt-0.5 shrink-0" />
      <p className="text-sm text-red-800 dark:text-red-200">{message}</p>
    </div>
  );
}
