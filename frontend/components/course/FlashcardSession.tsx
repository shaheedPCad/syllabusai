'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';
import type { FlashcardResponse } from '@/services/study';

interface FlashcardSessionProps {
  data: FlashcardResponse;
  onBack: () => void;
}

export function FlashcardSession({ data, onBack }: FlashcardSessionProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  const currentCard = data.flashcards[currentIndex];
  const progress = ((currentIndex + 1) / data.total_cards) * 100;

  const handleNext = () => {
    if (currentIndex < data.total_cards - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setIsFlipped(false);
    }
  };

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  const handleReset = () => {
    setCurrentIndex(0);
    setIsFlipped(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
        <div className="text-sm text-muted-foreground">
          Card {currentIndex + 1} of {data.total_cards}
        </div>
        <Button variant="outline" onClick={handleReset}>
          <RotateCcw className="mr-2 h-4 w-4" />
          Reset
        </Button>
      </div>

      {/* Progress Bar */}
      <Progress value={progress} className="h-2" />

      {/* Flashcard */}
      <Card
        className="min-h-[400px] cursor-pointer hover:shadow-lg transition-shadow"
        onClick={handleFlip}
      >
        <CardContent className="flex items-center justify-center min-h-[400px] p-8">
          <div className="text-center space-y-4">
            <div className="text-sm font-medium text-muted-foreground">
              {isFlipped ? 'Answer' : 'Question'}
            </div>
            <p className="text-2xl font-medium">
              {isFlipped ? currentCard.back : currentCard.front}
            </p>
            <p className="text-sm text-muted-foreground italic">
              Click to flip
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-center gap-4">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={currentIndex === 0}
        >
          <ChevronLeft className="mr-2 h-4 w-4" />
          Previous
        </Button>
        <Button
          onClick={handleNext}
          disabled={currentIndex === data.total_cards - 1}
        >
          Next
          <ChevronRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
