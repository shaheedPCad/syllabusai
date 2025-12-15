'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Lightbulb, Brain, GraduationCap, Target } from 'lucide-react';

export function StudyView() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <Card className="max-w-2xl w-full">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/10 rounded-lg">
              <Lightbulb className="h-8 w-8 text-primary" />
            </div>
            <div>
              <CardTitle className="text-2xl">Study Tools</CardTitle>
              <CardDescription className="mt-1">
                AI-generated flashcards and quizzes from your course materials
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-muted rounded-lg p-6 space-y-3">
            <div className="flex items-start gap-3">
              <Brain className="h-5 w-5 text-primary mt-0.5" />
              <div>
                <h3 className="font-semibold mb-1">Coming Soon</h3>
                <p className="text-sm text-muted-foreground">
                  The Study Suite is currently under development. Soon you'll be able to:
                </p>
              </div>
            </div>
            <ul className="ml-8 space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <GraduationCap className="h-4 w-4 text-primary mt-0.5" />
                <span>Generate flashcards automatically from your documents</span>
              </li>
              <li className="flex items-start gap-2">
                <Target className="h-4 w-4 text-primary mt-0.5" />
                <span>Take AI-generated quizzes to test your knowledge</span>
              </li>
              <li className="flex items-start gap-2">
                <Brain className="h-4 w-4 text-primary mt-0.5" />
                <span>Track your progress and identify weak areas</span>
              </li>
              <li className="flex items-start gap-2">
                <Lightbulb className="h-4 w-4 text-primary mt-0.5" />
                <span>Get personalized study recommendations</span>
              </li>
            </ul>
          </div>

          <div className="pt-4 text-center text-sm text-muted-foreground">
            Study materials will be generated from your uploaded documents using AI.
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
