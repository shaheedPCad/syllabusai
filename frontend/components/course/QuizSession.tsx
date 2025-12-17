'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, CheckCircle, XCircle } from 'lucide-react';
import type { QuizResponse } from '@/services/study';

interface QuizSessionProps {
  data: QuizResponse;
  onBack: () => void;
}

export function QuizSession({ data, onBack }: QuizSessionProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [hasAnswered, setHasAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const currentQuestion = data.questions[currentIndex];
  const progress = ((currentIndex + 1) / data.total_questions) * 100;

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null) return;

    setHasAnswered(true);
    if (selectedAnswer === currentQuestion.correct_answer_index) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < data.total_questions - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedAnswer(null);
      setHasAnswered(false);
    } else {
      setIsComplete(true);
    }
  };

  const isCorrect = selectedAnswer === currentQuestion.correct_answer_index;

  if (isComplete) {
    return (
      <div className="space-y-6">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Study Hub
        </Button>

        <Card className="text-center py-12">
          <CardHeader>
            <CardTitle className="text-3xl">Quiz Complete!</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-6xl font-bold text-primary">
              {score} / {data.total_questions}
            </div>
            <p className="text-muted-foreground">
              {score === data.total_questions && 'Perfect score! 🎉'}
              {score >= data.total_questions * 0.7 && score < data.total_questions && 'Great job! 👏'}
              {score < data.total_questions * 0.7 && 'Keep practicing! 💪'}
            </p>
            <Button onClick={onBack} className="mt-6">
              Return to Study Hub
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
        <div className="text-sm text-muted-foreground">
          Question {currentIndex + 1} of {data.total_questions}
        </div>
        <div className="text-sm font-medium">
          Score: {score}/{currentIndex + (hasAnswered ? 1 : 0)}
        </div>
      </div>

      {/* Progress */}
      <Progress value={progress} className="h-2" />

      {/* Question */}
      <Card>
        <CardHeader>
          <CardTitle>{currentQuestion.question}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <RadioGroup
            value={selectedAnswer !== null ? selectedAnswer.toString() : undefined}
            onValueChange={(value) => setSelectedAnswer(Number(value))}
            disabled={hasAnswered}
            key={currentIndex}
          >
            {currentQuestion.options.map((option, index) => {
              const isThisCorrect = index === currentQuestion.correct_answer_index;
              const showFeedback = hasAnswered;

              let bgColor = '';
              if (showFeedback) {
                if (isThisCorrect) {
                  bgColor = 'bg-green-50 dark:bg-green-950 border-green-500';
                } else if (index === selectedAnswer && !isThisCorrect) {
                  bgColor = 'bg-red-50 dark:bg-red-950 border-red-500';
                }
              }

              return (
                <div
                  key={index}
                  className={`flex items-center space-x-3 p-4 border rounded-lg ${bgColor}`}
                >
                  <RadioGroupItem value={index.toString()} id={`option-${index}`} />
                  <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                    {option}
                  </Label>
                  {showFeedback && isThisCorrect && (
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  )}
                  {showFeedback && index === selectedAnswer && !isThisCorrect && (
                    <XCircle className="h-5 w-5 text-red-600" />
                  )}
                </div>
              );
            })}
          </RadioGroup>

          {/* Explanation (shown after answering) */}
          {hasAnswered && (
            <div className={`p-4 rounded-lg ${isCorrect ? 'bg-green-50 dark:bg-green-950' : 'bg-yellow-50 dark:bg-yellow-950'}`}>
              <p className="font-medium mb-2">Explanation:</p>
              <p className="text-sm">{currentQuestion.explanation}</p>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-2">
            {!hasAnswered ? (
              <Button
                onClick={handleSubmitAnswer}
                disabled={selectedAnswer === null}
              >
                Submit Answer
              </Button>
            ) : (
              <Button onClick={handleNext}>
                {currentIndex < data.total_questions - 1 ? 'Next Question' : 'Finish Quiz'}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
